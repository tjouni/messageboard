from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from application.auth.models import User
from application.roles.models import Role
from application.categories.models import Category


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class NewUserForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1, max=144)])
    password = PasswordField("Password", [validators.Length(min=1, max=144)])
    name = StringField("Full name", [validators.Length(min=1, max=144)])
    email = StringField("E-mail", [validators.Length(min=1, max=144)])

    class Meta:
        csrf = False


class UpdateUserForm(FlaskForm):

    username = StringField("Username", [validators.Length(min=1, max=144)])
    new_password = PasswordField("New password", [validators.Length(max=144)])
    repeat_password = PasswordField(
        "Repeat password", [validators.Length(max=144)])
    name = StringField("Full name", [validators.Length(min=1, max=144)])
    email = StringField("E-mail", [validators.Length(min=1, max=144)])

    role = QuerySelectMultipleField(
        'Role',
        query_factory=lambda: Role.query.all(),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    category = QuerySelectMultipleField(
        'Category',
        query_factory=lambda: Category.query.all(),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    class Meta:
        csrf = False
