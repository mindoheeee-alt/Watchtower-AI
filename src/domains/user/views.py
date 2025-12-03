import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user
from flask_security import hash_password

from src.main import db
from src.domains.user.forms import SignUpForm
from src.domains.user.models import User

user_views = Blueprint(
    "user", __name__, template_folder="templates", static_folder="static"
)


@user_views.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=hash_password(form.password.data),
            active=True,
            fs_uniquifier=uuid.uuid4().hex,
        )

        if user.is_duplicate_email():
            flash("Email already registered")
            return redirect(url_for("user.signup"))

        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_page = request.args.get("next")
        if next_page is None or not next_page.startswith("/"):
            next_page = url_for("root.index")
        return redirect(next_page)
    return render_template("user/signup.html", form=form)
