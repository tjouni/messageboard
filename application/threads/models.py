from application import db


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)

    messages = db.relationship("Message", backref='thread', lazy=True)

    def __init__(self, title, category_id):
        self.title = title
        self.category_id = 0  # TODO
