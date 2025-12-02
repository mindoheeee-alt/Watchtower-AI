from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from src.auth.forms import LoginForm
from src.user.models import User

auth_views = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)


@auth_views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            next_page = request.args.get("next")
            if next_page is None or not next_page.startswith("/"):
                next_page = url_for("root.index")
            return redirect(next_page)
        else:
            flash("Invalid email or password")

    return render_template("auth/login.html", form=form)


@auth_views.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
