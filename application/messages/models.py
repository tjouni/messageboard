from application import db

print('models')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    message_text = db.Column(db.String(), nullable=False)

    def __init__(self, message_text, thread_id):
        self.message_text = message_text
        self.thread_id = thread_id
