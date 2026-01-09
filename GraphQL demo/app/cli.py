from bson.objectid import ObjectId
from flask.cli import FlaskGroup
from secrets import token_urlsafe
from werkzeug.security import generate_password_hash

from app import create_app
from app.db import db
from app.utils import is_valid_email

import os
import pandas as pd
import ast

cli = FlaskGroup(create_app=create_app)


@cli.command()
def create_user():
    valid_email = False
    while not valid_email:
        email = input("email: ")
        valid_email = is_valid_email(email)
        if not valid_email:
            print("Invalid email, please enter a valid email address...")
        existing_user = db.users.find_one({"email": email})
        if existing_user:
            print("Email address already is use...")

    valid_password = False
    while not valid_password:
        password_1 = input("password (leave empty to generate): ")
        if not password_1:
            password_1 = token_urlsafe()
            password_2 = password_1
            print(f"Generated password: {password_1}")
        else:
            password_2 = input("re-enter password: ")
        if password_1 != password_2:
            print("Passwords did not match...")
        if not password_1:
            print("Password can not be empty...")
        valid_password = True

    valid_senior = False
    while not valid_senior:
        senior = input("User is senior [y/N]: ") or "n"
        if senior.lower() not in ["y", "n", "yes", "no"]:
            print("Invalid input")
        if senior.lower()[0] == "y":
            senior = True
        else:
            senior = False
        valid_senior = True

    valid_admin = False
    while not valid_admin:
        admin = input("User is admin [y/N]: ") or "n"
        if admin.lower() not in ["y", "n", "yes", "no"]:
            print("Invalid input")
        if admin.lower()[0] == "y":
            admin = True
        else:
            admin = False
        valid_admin = True

    db.users.insert_one(
        {
            "email": email,
            "password": generate_password_hash(password_1),
            "admin": admin,
            "senior": senior,
        }
    )
    print(f"User with email {email} successfully created...")


@cli.command()
def reset_password():
    email = input("Provide the email of the account you want to reset: ")
    user = db.users.find_one({"email": email})
    if not user:
        print("Could not find user with the given email...")
        return 1

    valid_password = False
    while not valid_password:
        password_1 = input("password (leave empty to generate): ")
        if not password_1:
            password_1 = token_urlsafe()
            password_2 = password_1
            print(f"Generated password: {password_1}")
        else:
            password_2 = input("re-enter password: ")
        if password_1 != password_2:
            print("Passwords did not match...")
        if not password_1:
            print("Password can not be empty...")
        valid_password = True

    db.users.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"password": generate_password_hash(password_1)}},
    )
    print("Successfully reset password...")

@cli.command()
def upgrade_database():
    '''
    Upgrade the database so it supports using ObjectIds as references for dynamic fields instead of the field name.

    WARNING: Items in a collection where the link is already broken (because a configuration name has changed previously), cannot be updated.
    '''

    confirm = input("This will upgrade the database, are you sure you want to continue? [y/N]: ") or "n"

    if confirm.lower() not in ["y", "yes"]:
        print("Upgrade cancelled...")
        return 1

    configurations = db.configurations.find({"ConnectedCollection": "researchers"})

    for config in configurations:
        db.researchers.update_many(
            {config['name']: {"$exists": True}},
            {"$rename": { config['name']: f"dynamic_{config['_id']}" }}
        )

    configurations = db.configurations.find({"ConnectedCollection": "course"})

    for config in configurations:
        db.course.update_many(
            {config['name']: {"$exists": True}},
            {"$rename": { config['name']: f"dynamic_{config['_id']}" }}
        )

    configurations = db.configurations.find({"ConnectedCollection": "projects"})

    for config in configurations:
        db.projects.update_many(
            {config['name']: {"$exists": True}},
            {"$rename": { config['name']: f"dynamic_{config['_id']}" }}
        )

    configurations = db.configurations.find({"ConnectedCollection": "research_projects"})

    for config in configurations:
        db.research_projects.update_many(
            {config['name']: {"$exists": True}},
            {"$rename": { config['name']: f"dynamic_{config['_id']}" }}
        )

    print("Upgrade complete")

@cli.command()
def import_data():
    """
    Import data from csv files (which can be exported from DIPPER) into the database.
    """

    folder_path = input("Provide the folder path where the csv files are located: ")

    if not os.path.isdir(folder_path):
        print("Provided folder path is not a valid directory...")
        return 1
    
    # Read the csv files

    read_options = dict(na_values=[], keep_default_na=False)
    projects_csv = pd.read_csv(os.path.join(folder_path, "projects.csv"),  **read_options)
    research_projects_csv = pd.read_csv(os.path.join(folder_path, "research_projects.csv"),  **read_options)
    configurations_csv = pd.read_csv(os.path.join(folder_path, "configurations.csv"),  **read_options)
    researchers_csv = pd.read_csv(os.path.join(folder_path, "researchers.csv"),  **read_options)
    course_data_csv = pd.read_csv(os.path.join(folder_path, "course.csv"),  **read_options)

    # Insert the data into the database, and use the _id field as the ObjectId
    for collection_name, csv_data in [["projects", projects_csv],
                                      ["research_projects", research_projects_csv],
                                      ["configurations", configurations_csv],
                                      ["researchers", researchers_csv],
                                      ["course", course_data_csv]]:
        
        csv_data = csv_data.convert_dtypes()

        collection_data = csv_data.to_dict(orient="records")
        for item in collection_data:
            if "_id" in item:
                item["_id"] = ObjectId(item["_id"])

            if collection_name == "projects":
                item["project_image"] = ast.literal_eval(item["project_image"])

            # If field is empty, make it empty string
            for key, value in item.items():
                if pd.isna(value) or value == "":
                    item[key] = ""

            if collection_name == "projects":
                db.projects.insert_one(item)
            elif collection_name == "research_projects":
                db.research_projects.insert_one(item)
            elif collection_name == "configurations":
                db.configurations.insert_one(item)
            elif collection_name == "researchers":
                db.researchers.insert_one(item)
            elif collection_name == "course":
                db.course.insert_one(item)
    
    # Add the counters for the next project and research project codes, based on csv max values
    projectcodes = projects_csv["projectcode"].dropna()
    numeric_parts = projectcodes.str.replace("S-", "", regex=False).astype(int)
    max_project_code = numeric_parts.max()
    research_project_codes = research_projects_csv["research_project_code"].dropna()
    numeric_research_parts = research_project_codes.str.replace("R-", "", regex=False).astype(int)
    max_research_project_code = numeric_research_parts.max()
    db.counters.insert_one({"_id": "project_id", "sequence_value": int(max_project_code + 1)})
    db.counters.insert_one({"_id": "overproject_id", "sequence_value": int(max_research_project_code + 1)})

    print("Data imported successfully.")
