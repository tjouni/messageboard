from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.auth.models import User


class CategoryForm(FlaskForm):
    name = StringField("Category name")

    class Meta:
        csrf = False


class NewCategoryForm(FlaskForm):
    name = StringField("Category name", [validators.Length(min=1, max=50)])

    class Meta:
        csrf = False
