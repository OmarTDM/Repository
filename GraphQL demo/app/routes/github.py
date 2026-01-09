from flask import Blueprint, current_app, render_template
from flask_login import login_required
from ghapi.all import GhApi

bp = Blueprint("github", __name__)


@bp.route("/GitHub_urls")
@login_required
def github_repos():
    gh = GhApi()
    token = current_app.config.get("GITHUB_TOKEN")
    gh = GhApi(token=token)
    org = current_app.config.get("GITHUB_ORG")
    repos = gh.repos.list_for_org(org)
    return render_template("GitHub_urls.html", repos=repos)
