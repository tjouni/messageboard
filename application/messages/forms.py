from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class MessageForm(FlaskForm):
    message_text = TextAreaField(
        "Message text", [validators.Length(min=1, max=1500)])

    class Meta:
        csrf = False
