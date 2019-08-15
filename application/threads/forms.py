from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators


class ThreadForm(FlaskForm):
    title = StringField("Thread title", [validators.Length(min=1)])
    message_text = TextAreaField("Message text", [validators.Length(min=1)])

    class Meta:
        csrf = False
