from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.auth.models import User


class RoleForm(FlaskForm):
    name = StringField("Role name", [validators.Length(min=1, max=20)])

    class Meta:
        csrf = False
