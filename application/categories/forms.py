from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.auth.models import User


class CategoryForm(FlaskForm):
    name = StringField("Category name")

    class Meta:
        csrf = False
