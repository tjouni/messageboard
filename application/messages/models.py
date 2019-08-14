from application import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'),
                          nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                        nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    message_text = db.Column(db.String(), nullable=False)
    original_post = db.Column(db.Boolean, nullable=False)

    def __init__(self, message_text, thread_id, user_id, original_post=False):
        self.message_text = message_text
        self.thread_id = thread_id
        self.user_id = user_id
        self.original_post = original_post
