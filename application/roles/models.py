from application import db
from sqlalchemy.sql import text


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, role):
        self.role = role

    def __str__(self):
        return self.role

    @staticmethod
    def get_role_list():
        stmt = text("SELECT Role.id, Role.role,"
                    " (SELECT COUNT(a.id) FROM Role as r2"
                    "  JOIN user_role AS ur ON Role.id = ur.role_id"
                    "  JOIN account AS a ON ur.account_id = a.id) AS usercount"
                    " FROM Role"
                    " GROUP BY Role.id;")
        return db.session.execute(stmt)
