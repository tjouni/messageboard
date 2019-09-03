from application import db
from sqlalchemy.sql import text


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    threads = db.relationship("Thread", backref='category', lazy=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_category_list():
        stmt = text("SELECT Category.id, Category.name,"
                    " COUNT(Thread.id) as threadcount,"
                    " (SELECT COUNT(a.id) FROM Category AS c"
                    "  JOIN user_category AS uc ON c.id == uc.category_id AND c.id == Category.id"
                    "  JOIN account AS a ON uc.account_id == a.id)"
                    " AS usercount FROM Category"
                    " LEFT JOIN Thread ON Thread.category_id = Category.id"
                    " GROUP BY Category.id;")
        return db.session.execute(stmt)
