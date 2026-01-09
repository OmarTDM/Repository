import io
import pandas as pd
import zipfile
from bson.objectid import ObjectId
from flask import Blueprint, current_app, jsonify, render_template, send_file
from flask_login import login_required
from ghapi.all import GhApi
import re

from app.db import db

bp = Blueprint("downloads", __name__)


@bp.route("/downloads")
@login_required
def downloads():
    return render_template("downloads.html")


@bp.route("/downloadexcel")
@login_required
def downloadexcel():
    projects = list(db.projects.find())
    research_projects = list(db.research_projects.find())
    configurations = list(db.configurations.find())
    researchers = list(db.researchers.find())
    course_data = list(db.course.find())

    # Replace illegal characters from the column names (keys), as they will cause the export to fail
    allowed_chars = r"[^\w\s\.,;:?!'\"()\[\]{}\-_+=*/^%|&$€£¥@#~\\]"
    
    collections = [projects, research_projects, configurations, researchers, course_data]
    cleaned_collections = []

    for collection in collections:
        cleaned = [
            {
                re.sub(allowed_chars, "_", k) if isinstance(k, str) else k:
                re.sub(allowed_chars, "_", v) if isinstance(v, str) else v
                for k, v in item.items()
            }
            for item in collection
        ]
        cleaned_collections.append(cleaned)

    projects, research_projects, configurations, researchers, course_data = cleaned_collections

    # Add GitHub 
    token = current_app.config.get("GITHUB_TOKEN")
    gh = GhApi(token=token)
    org = current_app.config.get("GITHUB_ORG")
    repos = gh.repos.list_for_org(org)

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        pd.DataFrame(projects).to_excel(writer, sheet_name="Projects", index=False)
        pd.DataFrame(research_projects).to_excel(
            writer, sheet_name="Research projects", index=False
        )
        pd.DataFrame(configurations).to_excel(
            writer, sheet_name="Configurations", index=False
        )
        pd.DataFrame(researchers).to_excel(
            writer, sheet_name="Researchers", index=False
        )
        pd.DataFrame(course_data).to_excel(
            writer, sheet_name="Course Data", index=False
        )
        pd.DataFrame(repos).to_excel(writer, sheet_name="GitHub_urls", index=False)

    excel_buffer.seek(0)
    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name="mongo_data.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@bp.route("/download_csv_zip")
@login_required
def download_csv_zip():
    projects = pd.DataFrame(list(db.projects.find()))
    research_projects = pd.DataFrame(list(db.research_projects.find()))
    configurations = pd.DataFrame(list(db.configurations.find()))
    researchers = pd.DataFrame(list(db.researchers.find()))
    course_data = pd.DataFrame(list(db.course.find()))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        projects_csv = projects.to_csv(index=False, encoding="utf-8-sig")
        zip_file.writestr("projects.csv", projects_csv)

        research_projects_csv = research_projects.to_csv(
            index=False, encoding="utf-8-sig"
        )
        zip_file.writestr("research_projects.csv", research_projects_csv)

        configurations_csv = configurations.to_csv(index=False, encoding="utf-8-sig")
        zip_file.writestr("configurations.csv", configurations_csv)

        researchers_csv = researchers.to_csv(index=False, encoding="utf-8-sig")
        zip_file.writestr("researchers.csv", researchers_csv)

        course_data_csv = course_data.to_csv(index=False, encoding="utf-8-sig")
        zip_file.writestr("course.csv", course_data_csv)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="mongo_data.zip",
        mimetype="application/zip",
    )


@bp.route("/download_json")
@login_required
def download_json():
    projects = list(db.projects.find())

    for project in projects:
        if "project_image" in project and project["project_image"]:
            project["project_image"] = str(project["_id"]) + ".webp"

        if "research_project" in project:
            research_project = db.research_projects.find_one(
                {"_id": ObjectId(project["research_project"])}
            )
            research_project.pop("_id", None)
            project["research_project"] = research_project

        if "researcher" in project:
            researcher = db.researchers.find_one(
                {"_id": ObjectId(project["researcher"])}
            )
            researcher.pop("_id", None)
            project["researcher"] = researcher

        if "course" in project:
            course_obj = db.course.find_one({"_id": ObjectId(project["course"])})
            course_obj.pop("_id", None)
            project["course"] = course_obj

        if "GitHub_url" in project and project["GitHub_url"]:
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

        project.pop("_id", None)

    return jsonify(projects)
