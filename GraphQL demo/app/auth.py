from bson.objectid import ObjectId
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    LoginManager,
    login_required,
)
from flask_wtf import FlaskForm
from functools import wraps
from urllib.parse import urlsplit
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import BooleanField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, equal_to

from app.db import db

login = LoginManager()
login.login_view = "auth.login_route"
login.login_message = "Please log in to access this page."


bp = Blueprint("auth", __name__)


class User:
    id: str
    email: str
    password_hash: str
    admin: bool
    senior: bool
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(
        self,
        _id: str,
        email: str,
        password_hash: str,
        admin: bool = False,
        senior: bool = False,
    ):
        self.id = _id
        self.email = email
        self.password_hash = password_hash
        self.admin = admin
        self.senior = senior

    def get_id(self):
        return self.email

    def is_admin(self):
        return self.admin


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if not current_user.is_anonymous:
            if current_user.admin:
                return func(*args, **kw)
        else:
            return redirect(url_for("auth.login_route"))
        abort(403)

    return wrapper


def senior_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if not current_user.is_anonymous:
            if current_user.senior or current_user.admin:
                return func(*args, **kw)
        else:
            return redirect(url_for("auth.login_route"))
        abort(403)

    return wrapper


@login.user_loader
def load_user(email):
    user = db.users.find_one({"email": email})
    if not user:
        return None
    return User(
        user["_id"],
        user["email"],
        user["password"],
        user["admin"],
        user["senior"] if "senior" in user else False,
    )


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current password", validators=[DataRequired()])
    password_1 = PasswordField("Password", validators=[DataRequired()])
    password_2 = PasswordField(
        "Password repeat", validators=[DataRequired(), equal_to("password_1")]
    )
    submit = SubmitField("Change Password")


@bp.route("/login", methods=["GET", "POST"])
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.find_one({"email": form.email.data})
        if not user or not check_password_hash(user["password"], form.password.data):
            flash("Wrong email or password")
            return redirect(url_for("auth.login_route"))
        login_user(
            User(
                user["_id"],
                user["email"],
                user["password"],
                user["admin"],
                user["senior"] if "senior" in user else False,
            ),
            remember=form.remember.data,
        )
        flash("Login successful")
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout_route():
    logout_user()
    flash("Logout successful")
    return redirect(url_for("index"))


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile_route():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.old_password.data):
            flash("Wrong password")
            return redirect(url_for("auth.profile"))
        db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {"password": generate_password_hash(form.password_1.data)}},
        )
        flash("Changed password")
        return redirect(url_for("auth.profile_route"))
    return render_template("auth/profile.html", form=form)
