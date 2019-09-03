from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, validators


class ThreadForm(FlaskForm):
    title = StringField("Thread title", [validators.Length(min=1)])
    message_text = TextAreaField("Message text", [validators.Length(min=1)])
    thread_category = SelectField("Thread category", coerce=int)

    class Meta:
        csrf = False
