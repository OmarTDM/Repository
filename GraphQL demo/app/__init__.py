import os
from flask import Flask, render_template
from flask_login import login_required
from typing import Union

from app import routes
from app.auth import login, bp as auth_bp
from app.db import client, db
from app.routes import (
    configuration,
    courses,
    downloads,
    github,
    projects,
    research_projects,
    researchers,
)


def create_app(config_obj: Union[str, object] = "app.config") -> Flask:
    # Use the repository-level templates and static folders (not package-local)
    pkg_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(pkg_dir, ".."))
    templates_dir = os.path.join(project_root, "templates")
    static_dir = os.path.join(project_root, "static")
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    app.config.from_object(config_obj)

    static_temp_dir = os.path.join(app.config.get("BASEDIR"), "static/temp")
    print(static_temp_dir)
    if not os.path.exists(static_temp_dir):
        os.makedirs(static_temp_dir)

    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Optionally disable authentication for local testing by setting
    # the environment variable DISABLE_AUTH=true
    if os.environ.get("DISABLE_AUTH", "false").lower() in ("1", "true", "yes"):
        import flask_login as _fl

        def _noop_login_required(func=None, **kwargs):
            if func is None:
                def _decorator(f):
                    return f

                return _decorator
            return func

        _fl.login_required = _noop_login_required
        print("Warning: Authentication disabled (DISABLE_AUTH=true)")

    @app.route("/")
    @login_required
    def index():
        return render_template("index.html")

    app.register_blueprint(auth_bp)
    app.register_blueprint(configuration.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(downloads.bp)
    app.register_blueprint(github.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(research_projects.bp)
    app.register_blueprint(researchers.bp)
    # Register stats and graphql blueprints (local additions)
    try:
        from app.routes import stats as stats_bp
        app.register_blueprint(stats_bp.bp)
    except Exception:
        pass
    try:
        from app.routes import graphql as graphql_bp
        app.register_blueprint(graphql_bp.bp)
    except Exception:
        pass

    login.init_app(app)

    # If auth is disabled, unwrap decorated view functions (remove login_required wrapper)
    if os.environ.get("DISABLE_AUTH", "false").lower() in ("1", "true", "yes"):
        for endpoint, func in list(app.view_functions.items()):
            try:
                original = getattr(func, "__wrapped__", None)
                if original:
                    app.view_functions[endpoint] = original
            except Exception:
                pass

    return app
