from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from application.auth.models import User


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class NewUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1)])
    password = PasswordField("Password", [validators.Length(min=1)])
    name = StringField("Full name", [validators.Length(min=1)])
    email = StringField("E-mail", [validators.Length(min=1)])

    class Meta:
        csrf = False


class UpdateUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1)])
    new_password = PasswordField("New password")
    repeat_password = PasswordField("Repeat password")
    name = StringField("Full name", [validators.Length(min=1)])
    email = StringField("E-mail", [validators.Length(min=1)])

    class Meta:
        csrf = False
