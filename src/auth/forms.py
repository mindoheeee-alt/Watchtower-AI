from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired("Email is required"), Email("Email is invalid")],
    )
    password = PasswordField(
        "Password", validators=[DataRequired("Password is required")]
    )
    submit = SubmitField("Login")
