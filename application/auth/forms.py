from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class AddUserForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    name = StringField("Full name")
    email = StringField("E-mail")

    class Meta:
        csrf = False
