import pandas as pd
from bson.objectid import ObjectId
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from app.auth import admin_required
from app.db import db

bp = Blueprint("courses", __name__)


@bp.route("/course")
@login_required
def course():
    courses = db.course.find()
    df = pd.DataFrame(list(courses))

    # Replace dynamic fields with configuration names
    configurations = db.configurations.find(
        {"ConnectedCollection": "course"}
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
        "course.html", table_columns=table_columns, table_rows=table_rows
    )


@bp.route("/create_course", methods=["GET", "POST"])
@admin_required
def create_course():
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "course"}
    )  # Fetch configurations where inuse=True and ConnectedCollection is 'course'
    if request.method == "POST":
        name = request.form["name"]

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

        db.course.insert_one({"name": name, **dynamic_fields})

        return redirect(url_for("courses.course"))
    else:
        return render_template("createcourse.html", configurations=configurations)


@bp.route("/edit_course/<string:id>", methods=["GET", "POST"])
@admin_required
def edit_course(id):
    course = db.course.find_one({"_id": ObjectId(id)})
    configurations = db.configurations.find(
        {"inuse": True, "ConnectedCollection": "course"}
    )

    if request.method == "POST":
        name = request.form["name"]

        # Check for duplicate name
        existing_course = db.course.find_one({"name": name})
        if existing_course and str(existing_course["_id"]) != id:
            flash(f"The Course with name '{name}' already exists.", "error")  # type: ignore
            return render_template(
                "editcourse.html", course=course, configurations=configurations
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

        dynamic_fields["name"] = name
        db.course.update_one({"_id": ObjectId(id)}, {"$set": dynamic_fields})
        return redirect(
            url_for("courses.course")
        )  # Change to your actual Course list route
    else:
        return render_template(
            "editcourse.html", course=course, configurations=configurations
        )
