from application import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_text = db.Column(db.String(), nullable=False)

    threads = db.relationship("Thread", backref='category', lazy=True)

    def __init__(self, name):
        self.name = name
