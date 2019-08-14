from application import db
from application.models import Base


class Thread(Base):
    title = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False, index=True)

    messages = db.relationship("Message", backref='thread', lazy=True)

    def __init__(self, title, category_id):
        self.title = title
        self.category_id = 0  # TODO
