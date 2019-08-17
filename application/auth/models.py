from application import db
from application.models import Base
from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    email = db.Column(db.String(144), nullable=False)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_messages(self):
        return db.relationship('Message', backref='account', lazy=True)

    @staticmethod
    def get_user_list():
        stmt = text("SELECT Account.id, Account.username, Account.name, Account.email,"
                    " COUNT(Message.id) as messagecount,"
                    " (SELECT COUNT(DISTINCT m2.id) FROM Message AS m2"
                    "  JOIN Account AS a2 ON m2.user_id = Account.id"
                    "  WHERE m2.original_post = true) AS threadcount FROM Account "
                    " LEFT JOIN Message ON Message.user_id = Account.id  "
                    " GROUP BY Account.id;"
                    )
        return db.engine.execute(stmt)
