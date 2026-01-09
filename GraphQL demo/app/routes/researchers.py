import pandas as pd
from bson.objectid import ObjectId
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from app.auth import admin_required
from app.db import db
from app.utils import is_valid_email

bp = Blueprint("researchers", __name__)


@bp.route("/researchers")
@login_required
def researchers():
    researchers = db.researchers.find()
    df = pd.DataFrame(list(researchers))

    # Replace dynamic fields with configuration names
    configurations = db.configurations.find(
        {"ConnectedCollection": "researchers"}
    )

    for config in configurations:
        attribute_object_id = config["_id"]
        attribute_name = config["name"]
        dynamic_field_key = f"dynamic_{attribute_object_id}"
        if dynamic_field_key in df.columns:
            df.rename(columns={dynamic_field_key: attribute_name}, inplace=True)
        
        # Check if the dynamic field is a Checkboxes type
        if config["type"] == "Checkboxes":
            # Convert the list of checkboxes into a comma-separated string
            try:
                df[attribute_name] = df[attribute_name].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
            except:
                pass # Skip if the field is not present (which can happen for new configurations)

    table_columns = df.columns.tolist()
    table_rows = df.to_dict(orient="records")
    return render_template(
        "researchers.html", table_columns=table_columns, table_rows=table_rows
    )


@bp.route("/create_researcher", methods=["GET", "POST"])
@admin_required
def create_researcher():
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "researchers"}
    )  # Fetch configurations where inuse=True
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # Validate email address
        if not is_valid_email(email):
            return render_template("error.html", error_message="Invalid email address.")

        # Process dynamic fields
        dynamic_fields = {}
        for config in configurations:
            attribute_name = config["name"]
            attribute_type = config["type"]
            attribute_object_id = config["_id"]
            if attribute_type == "String":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form[attribute_name]
            elif attribute_type == "Integer":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = int(request.form[attribute_name])
            elif attribute_type == "Double":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = float(request.form[attribute_name])
            elif attribute_type == "Boolean":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = bool(request.form.get(attribute_name))
            elif attribute_type == "Date":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form[attribute_name]
            elif attribute_type == "ObjectId":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = ObjectId(request.form[attribute_name])
            elif attribute_type == "Array":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form[attribute_name]
            elif attribute_type == "Checkboxes":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form.getlist(attribute_name)
            elif attribute_type == "Checkboxes":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form.getlist(attribute_name)
            elif attribute_type == "Binary Data":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.files[attribute_name].read()
            elif attribute_type == "Undefined":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None
            elif attribute_type == "Null":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None

        # Save researcher to the database
        db.researchers.insert_one({"name": name, "email": email, **dynamic_fields})

        return redirect(url_for("researchers.researchers"))
    else:
        return render_template("createresearcher.html", configurations=configurations)


@bp.route("/edit_researcher/<string:id>", methods=["GET", "POST"])
@admin_required
def edit_researcher(id):
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "researchers"}
    )  # Fetch configurations where inuse=True
    researcher = db.researchers.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # Validate email address
        if not is_valid_email(email):
            return render_template("error.html", error_message="Invalid email address.")

        # Process dynamic fields
        dynamic_fields = {}
        for config in configurations:
            attribute_name = config["name"]
            attribute_type = config["type"]
            attribute_object_id = config["_id"]
            if attribute_type == "String":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form[attribute_name]
            elif attribute_type == "Integer":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = int(request.form[attribute_name])
            elif attribute_type == "Double":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = float(request.form[attribute_name])
            elif attribute_type == "Boolean":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = bool(request.form.get(attribute_name))
            elif attribute_type == "Date":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form[attribute_name]
            elif attribute_type == "ObjectId":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = ObjectId(request.form[attribute_name])
            elif attribute_type == "Array":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form[attribute_name]
            elif attribute_type == "Checkboxes":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form.getlist(attribute_name)
            elif attribute_type == "Checkboxes":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.form.getlist(attribute_name)
            elif attribute_type == "Binary Data":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.files[attribute_name].read()
            elif attribute_type == "Undefined":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None
            elif attribute_type == "Null":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None

        # Update researcher in the database
        db.researchers.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": name, "email": email, **dynamic_fields}},
        )

        return redirect(url_for("researchers.researchers"))
    else:
        return render_template(
            "editresearcher.html", configurations=configurations, researcher=researcher
        )
