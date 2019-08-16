from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class UserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1)])
    password = PasswordField("Password", [validators.Length(min=1)])
    name = StringField("Full name", [validators.Length(min=1)])
    email = StringField("E-mail", [validators.Length(min=1)])

    class Meta:
        csrf = False
