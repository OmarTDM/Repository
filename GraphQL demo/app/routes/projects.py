import os
import pandas as pd
from bson.objectid import ObjectId
from flask import (
    abort,
    Blueprint,
    current_app,
    render_template,
    redirect,
    request,
    url_for,
)
from flask_login import login_required
from ghapi.all import GhApi

from app.db import db
from app.utils import (
    convert_image_to_webp,
    format_studentproject_number,
    get_next_project_code,
)

from app.utils import github_slugify

bp = Blueprint("projects", __name__)


@bp.route("/projects")
@login_required
def projects():
    query = request.args.get('query')
    field = request.args.get('field')
    
    projects = list(db.projects.find())
    research = list(db.research_projects.find())
    
    for project in projects:
        if "research_project" in project:
            research_project = db.research_projects.find_one(
                {"_id": ObjectId(project["research_project"])}
            )
            project["research_project"] = (
                research_project["research_project"] if research_project else None
            )

        if "researcher" in project:
            researcher = db.researchers.find_one(
                {"_id": ObjectId(project["researcher"])}
            )
            project["researcher"] = researcher["name"] if researcher else None

        if "course" in project:
            course_obj = db.course.find_one({"_id": ObjectId(project["course"])})
            project["course"] = course_obj["name"] if course_obj else None

        if "project_image" in project and project["project_image"]:
            with open("app/static/temp/" + str(project["_id"]) + ".webp", "wb") as f:
                f.write(project["project_image"])
            project["imagepath"] = str(project["_id"]) + ".webp"

    # Filter projects based on the search query
    if query:
        if field == "any":
            projects = [project for project in projects if any(query.lower() in str(value).lower() for value in project.values())]
        else:
            projects = [project for project in projects if query.lower() in str(project.get(field, '')).lower()]

    # Reverse the list of projects
    projects.reverse()

    df = pd.DataFrame(projects)
    table_columns = df.columns.tolist()
    table_rows = df.to_dict(orient="records")

    return render_template(
        "projects.html",
        table_columns=table_columns,
        table_rows=table_rows,
        research=research,
    )


@bp.route("/create_project", methods=["GET", "POST"])
@login_required
def create_project():
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "projects"}
    )
    research_projects = db.research_projects.find()
    researchers = db.researchers.find()
    course = db.course.find()
    if request.method == "POST":
        name = request.form["title"]
        project_motive = request.form["project_motive"]
        project_goal = request.form["project_goal"]
        target_result = request.form["target_result"]
        students = request.form["students"]
        selected_research_project = request.form["research_project"]
        selected_researcher = request.form["researcher"]
        selected_course = request.form["course"]

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
            elif attribute_type == "Binary Data":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.files[attribute_name].read()
            elif attribute_type == "Undefined":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None
            elif attribute_type == "Null":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None

        # Check if project_image is uploaded
        if "project_image" in request.files and request.files["project_image"]:
            project_image = request.files.get("project_image")
            image_stream = project_image.stream
        else:
            # Use default image if no image is uploaded (app/static/logo.png)
            image_stream = open("app/static/logo.png", "rb")

        image_binary = convert_image_to_webp(image_stream)

        project_code = format_studentproject_number(get_next_project_code())

        if request.form.get("githubenabled"):
            private = True
            auto_init = True

            gh = GhApi(token=current_app.config.get("GITHUB_TOKEN"))
            org = current_app.config.get("GITHUB_ORG")

            repos = gh.repos.list_for_org(org)
            if any(repo.name.lower() == github_slugify(name).lower() for repo in repos):
                error_message = (
                    f"Repository '{name}' already exists in the organization."
                )
                return render_template("error.html", error_message=error_message)

            repo = gh.repos.create_in_org(
                org,
                name=name,
                description="A DI-Lab Project",
                private=private,
                auto_init=auto_init,
            )

            db.projects.insert_one(
                {
                    "title": name,
                    "projectcode": project_code,
                    "project_motive": project_motive,
                    "project_goal": project_goal,
                    "target_result": target_result,
                    "students": students,
                    "GitHub_url": repo.html_url,
                    "research_project": selected_research_project,
                    "researcher": selected_researcher,
                    "course": selected_course,
                    "project_image": image_binary,
                    **dynamic_fields,
                }
            )
        else:
            GitHub_url = request.form.get("GitHub_url")
            db.projects.insert_one(
                {
                    "title": name,
                    "projectcode": project_code,
                    "project_motive": project_motive,
                    "project_goal": project_goal,
                    "target_result": target_result,
                    "students": students,
                    "GitHub_url": GitHub_url,
                    "research_project": selected_research_project,
                    "researcher": selected_researcher,
                    "course": selected_course,
                    "project_image": image_binary,
                    **dynamic_fields,
                }
            )

        return redirect(url_for("projects.projects"))
    else:
        return render_template(
            "createproject.html",
            configurations=configurations,
            research_projects=research_projects,
            researchers=researchers,
            course=course,
        )


@bp.route("/edit_project/<string:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project = db.projects.find_one({"_id": ObjectId(id)})
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "projects"}
    )
    research_projects = db.research_projects.find()
    researchers = db.researchers.find()
    course = db.course.find()

    if "project_image" in project and project["project_image"]:
        with open("app/static/temp/" + str(project["_id"]) + ".webp", "wb") as f:
            f.write(project["project_image"])
        project["imagepath"] = str(project["_id"]) + ".webp"

    if request.method == "POST":
        name = request.form["title"]
        project_motive = request.form["project_motive"]
        project_goal = request.form["project_goal"]
        target_result = request.form["target_result"]
        students = request.form["students"]
        selected_research_project = request.form["research_project"]
        selected_researcher = request.form["researcher"]
        selected_course = request.form["course"]
        GitHub_url = request.form["GitHub_url"]

        # Check if project_image is uploaded
        if "project_image" in request.files and request.files["project_image"]:
            project_image = request.files.get("project_image")
            image_stream = project_image.stream
            image_binary = convert_image_to_webp(image_stream)
            db.projects.update_one(
                {"_id": ObjectId(id)}, {"$set": {"project_image": image_binary}}
            )

        # Remove ending slashes before saving. If we do not do this, the application
        # will have issues later, because it finds the organization and repository
        # based on separating on slashes.
        try:
            if GitHub_url[-1] == "/":
                GitHub_url = GitHub_url[:-1]
        except:
            pass

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
            elif attribute_type == "Binary Data":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = request.files[attribute_name].read()
            elif attribute_type == "Undefined":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None
            elif attribute_type == "Null":
                dynamic_fields[f"dynamic_{attribute_object_id}"] = None

        db.projects.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "title": name,
                    "target_result": target_result,
                    "project_motive": project_motive,
                    "project_goal": project_goal,
                    "students": students,
                    "GitHub_url": GitHub_url,
                    "research_project": selected_research_project,
                    "researcher": selected_researcher,
                    "course": selected_course,
                    **dynamic_fields,
                }
            },
        )
        return redirect(url_for("projects.projects"))
    else:
        return render_template(
            "editproject.html",
            project=project,
            configurations=configurations,
            research_projects=research_projects,
            researchers=researchers,
            course=course,
        )


@bp.route("/delete_project/<string:id>", methods=["POST"])
@login_required
def delete_project(id):
    project = db.projects.find_one({"_id": ObjectId(id)})
    if not project:
        return "Project not found", 404

    # Ask for confirmation before deleting the project
    return render_template("deleteconfirmation.html", project=project)


@bp.route("/delete_project_confirm/<string:id>", methods=["POST"])
@login_required
def delete_project_confirm(id):
    db.projects.delete_one({"_id": ObjectId(id)})

    return redirect(url_for("projects.projects"))


@bp.route("/project_details/<string:id>")
@login_required
def project_details(id):
    project = db.projects.find_one({"_id": ObjectId(id)})
    configurations_cursor = db.configurations.find(
        {
            "$or": [
                {"ConnectedCollection": "projects"},
                {"ConnectedCollection": "course"},
                {"ConnectedCollection": "research_projects"},
                {"ConnectedCollection": "researchers"}
            ]
        }
    )

    if not project:
        # Handle case where project with given ID is not found
        abort(404)

    if "project_image" in project and project["project_image"]:
        with open("app/static/temp/" + str(project["_id"]) + ".webp", "wb") as f:
            f.write(project["project_image"])
        project["project_image"] = str(project["_id"]) + ".webp"

    # Fetch related objects and add them to the project dictionary
    if "research_project" in project:
        research_project = db.research_projects.find_one(
            {"_id": ObjectId(project["research_project"])}
        )
        project["research_project"] = research_project

    if "researcher" in project:
        researcher = db.researchers.find_one({"_id": ObjectId(project["researcher"])})
        project["researcher"] = researcher

    if "course" in project:
        course_obj = db.course.find_one({"_id": ObjectId(project["course"])})
        project["course"] = course_obj

    if "GitHub_url" in project:
        try:
            token = current_app.config.get("GITHUB_TOKEN")
            gh = GhApi(token=token)

            github_url = project["GitHub_url"]
            owner, repo_name = github_url.split("/")[-2:]

            repo = gh.repos.get(owner=owner, repo=repo_name)

            contributors = gh.repos.list_contributors(owner=owner, repo=repo_name)
            contributors_list = [contributor.login for contributor in contributors]

            project["github_info"] = {
                "name": repo.name,
                "description": repo.description,
                "owner": repo.owner.login,
                "visibility": "Private" if repo.private else "Public",
                "language": repo.language,
                "contributors": contributors_list,
                "topics": ", ".join(repo.topics),
            }
        except:
            project["github_info"] = {"Info": "GitHub Repository Not Found"}
    else:
        project["github_info"] = {"Info": "GitHub Repository Not Found"}

    # Create a dictionary to map configuration IDs to names
    configurations = {}

    for config in configurations_cursor:
        configurations[str(config["_id"])] = config["name"]

        # If type is Checkboxes, convert the value to a list
        if config["type"] == "Checkboxes":
            # Check if the field exists in the project
            if "dynamic_" + str(config["_id"]) in project:
                project["dynamic_" + str(config["_id"])] = ", ".join(project["dynamic_" + str(config["_id"])])

    return render_template("projectdetails.html", project=project, configurations=configurations)
