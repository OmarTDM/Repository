import pandas as pd
from bson.objectid import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.auth import senior_required
from app.db import db
from app.utils import format_research_project_number, get_next_research_project_code

bp = Blueprint("research_projects", __name__)


@bp.route("/research_projects")
@login_required
def research_projects():
    research_projects = db.research_projects.find()
    df = pd.DataFrame(list(research_projects))

    # Replace dynamic fields with configuration names
    configurations = db.configurations.find(
        {"ConnectedCollection": "research_projects"}
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
        "research.html", table_columns=table_columns, table_rows=table_rows
    )


@bp.route("/create_research_project", methods=["GET", "POST"])
@senior_required
def create_research_project():
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "research_projects"}
    )  # Fetch configurations where inuse=True
    if request.method == "POST":
        research_project = request.form["research_project"]

        # Check for duplicate research_project
        if db.research_projects.find_one({"research_project": research_project}):
            flash(f"The research project '{research_project}' already exists.", "error")  # type: ignore
            return render_template("createresearch.html", configurations=configurations)

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

        researchprojectcode = format_research_project_number(
            get_next_research_project_code()
        )

        db.research_projects.insert_one(
            {
                "research_project": research_project,
                "research_project_code": researchprojectcode,
                **dynamic_fields,
            }
        )
        return redirect(url_for("research_projects.research_projects"))
    else:
        return render_template("createresearch.html", configurations=configurations)


@bp.route("/edit_research_project/<string:id>", methods=["GET", "POST"])
@senior_required
def edit_research_project(id):
    project = db.research_projects.find_one({"_id": ObjectId(id)})
    print(project)
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "research_projects"}
    )

    if request.method == "POST":
        research_project = request.form["research_project"]

        # Check for duplicate research_project
        existing_project = db.research_projects.find_one(
            {"research_project": research_project}
        )
        if existing_project and str(existing_project["_id"]) != id:
            flash(f"The research project '{research_project}' already exists.", "error")  # type: ignore
            return render_template(
                "editresearch.html", project=project, configurations=configurations
            )

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

        dynamic_fields["research_project"] = research_project
        db.research_projects.update_one({"_id": ObjectId(id)}, {"$set": dynamic_fields})
        return redirect(url_for("research_projects.research_projects"))
    else:
        return render_template(
            "editresearch.html", project=project, configurations=configurations
        )
