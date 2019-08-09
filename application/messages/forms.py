from flask_wtf import FlaskForm
from wtforms import StringField, validators


class MessageForm(FlaskForm):
    message_text = StringField("Message text", [validators.Length(min=1)])

    class Meta:
        csrf = False
