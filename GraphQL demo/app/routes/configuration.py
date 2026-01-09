import math
import re
import pandas as pd
from bson.objectid import ObjectId
from flask import Blueprint, redirect, render_template, request, url_for

from app.db import bson_types, db
from app.auth import admin_required

bp = Blueprint("configuration", __name__)

DEFAULT_FIELDS = {
    "projects": [
        "_id,",
        "title", 
        "projectcode", 
        "project_motive", 
        "project_goal", 
        "target_result", 
        "students", 
        "GitHub_url", 
        "research_project", 
        "researcher", 
        "course", 
        "project_image"
    ],
    "research_projects": [
        "_id",
        "research_project",
        "research_project_code"
    ],
    "researchers": [
        "_id",
        "name"
    ],
    "course": [
        "_id",
        "name"
    ]
}

@bp.route("/configuration")
@admin_required
def configuration():
    configurations = db.configurations.find()
    df = pd.DataFrame(list(configurations))
    table_columns = df.columns.tolist()
    table_rows = df.to_dict(orient="records")
    return render_template(
        "configuration.html", table_columns=table_columns, table_rows=table_rows
    )


@bp.route("/makeconfig", methods=["GET", "POST"])
@admin_required
def makeconfig():
    if request.method == "POST":
        attribute_name = request.form["attributename"]
        attribute_type = request.form["attributetype"]
        attribute_inuse = request.form.get("inuse", False)
        attribute_inuse = True if attribute_inuse == "on" else False

        attribute_required = request.form.get("required", False)
        attribute_required = True if attribute_required == "on" else False

        connected_collection = request.form["ConnectedCollection"]

        # Check if configuration already exists
        existing_config = db.configurations.find_one({"name": attribute_name, "ConnectedCollection": connected_collection})
        if existing_config:
            return render_template("error.html", error_message="A configuration with this name already exists in the selected collection")
        
        if attribute_name in DEFAULT_FIELDS[connected_collection]:
            return render_template("error.html", error_message="This field is already in use by the system and cannot be added as a custom field")

        # Common configuration data
        config_data = {
            "name": attribute_name,
            "type": attribute_type,
            "inuse": attribute_inuse,     
            "required": attribute_required,  
            "ConnectedCollection": connected_collection,
        }

        # Handle Array or Checkboxes
        if attribute_type == "Array" or attribute_type == "Checkboxes":
            array_contents = request.form.getlist("array_contents[]")
            array_contents = list(set(array_contents))  # Remove duplicates
            config_data["ArrayContents"] = array_contents

        # Handle regex if enabled: save pattern, custom error and example placeholder
        if "regex_enabled" in request.form:
            regex_value = request.form.get("regex_pattern", "").strip()
            regex_error = request.form.get("regex_error", "").strip()
            regex_example = request.form.get("regex_example", "").strip()

            if regex_value:
                config_data["regex_pattern"] = regex_value
            if regex_error:
                config_data["regex_error_message"] = regex_error
            if regex_example:
                config_data["example_placeholder"] = regex_example

        db.configurations.insert_one(config_data)
        return redirect(url_for("configuration.configuration"))
    else:
        collection_names = ["course", "researchers", "projects", "research_projects"]

        return render_template(
            "makeconfig.html", bson_types=bson_types, collections=collection_names
        )


@bp.route("/config_inuse/<string:id>", methods=["POST"])
@admin_required
def config_inuse(id):
    config = db.configurations.find_one({"_id": ObjectId(id)})
    if config:
        inuse = config.get("inuse", math.nan)
        if inuse != inuse or not inuse:
            db.configurations.update_one({"_id": ObjectId(id)}, {"$set": {"inuse": True}})
        else:
            db.configurations.update_one({"_id": ObjectId(id)}, {"$set": {"inuse": False}})
    return redirect(url_for("configuration.configuration"))


@bp.route("/editconfig/<string:id>", methods=["GET", "POST"])
@admin_required
def editconfig(id):
    configuration = db.configurations.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        attribute_name = request.form["attributename"]
        attribute_type = configuration["type"]
        attribute_inuse = request.form.get("inuse", False)
        attribute_inuse = True if attribute_inuse == "on" else False
        attribute_required = request.form.get("required", False)
        attribute_required = True if attribute_required == "on" else False

        connected_collection = configuration["ConnectedCollection"]

        update_data = {
            "name": attribute_name,
            "type": attribute_type,
            "inuse": attribute_inuse,
            "required": attribute_required,   
            "ConnectedCollection": connected_collection,
        }

        if attribute_type == "Array" or attribute_type == "Checkboxes":
            array_contents = request.form.getlist("array_contents[]")
            array_contents = list(set(array_contents))
            update_data["ArrayContents"] = array_contents

        # Update regex fields: if regex_enabled present -> set values (may be empty), else clear them
        if "regex_enabled" in request.form:
            regex_value = request.form.get("regex_pattern", "").strip()
            regex_error = request.form.get("regex_error", "").strip()
            regex_example = request.form.get("regex_example", "").strip()

            update_data["regex_pattern"] = regex_value if regex_value else ""
            update_data["regex_error_message"] = regex_error if regex_error else ""
            update_data["example_placeholder"] = regex_example if regex_example else ""
        else:
            # regex disabled — clear stored regex fields
            update_data["regex_pattern"] = ""
            update_data["regex_error_message"] = ""
            update_data["example_placeholder"] = ""

        db.configurations.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return redirect(url_for("configuration.configuration"))
    else:
        collection_names = db.list_collection_names()
        collection_names = [name for name in collection_names if name != "configurations"]

        return render_template(
            "editconfig.html",
            bson_types=bson_types,
            configuration=configuration,
            collections=collection_names,
        )
