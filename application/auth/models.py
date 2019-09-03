from application import db
from application.models import Base
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.sql import text


association_table = Table('user_role', Base.metadata,
                          Column('account_id', Integer,
                                 ForeignKey('account.id')),
                          Column('role_id', Integer, ForeignKey('role.id'))
                          )

association_table2 = Table('user_category', Base.metadata,
                           Column('account_id', Integer,
                                  ForeignKey('account.id')),
                           Column('category_id', Integer,
                                  ForeignKey('category.id'))
                           )


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    email = db.Column(db.String(144), nullable=False)

    roles = db.relationship("Role", secondary="user_role",
                            backref=db.backref('accounts', lazy=True))
    categories = db.relationship("Category", secondary="user_category",
                                 backref=db.backref('accounts', lazy=True))

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

    def is_admin(self):
        for role in self.roles:
            if role.role == 'admin':
                return True
        return False

    def get_category_ids(self):
        ids = []
        for category_row in self.categories:
            ids.append(category_row.id)
        return ids

    @staticmethod
    def get_user_list():
        '''Return a list with basic user information and statistics'''
        stmt = text("SELECT Account.id, Account.username, Account.name, Account.email,"
                    " COUNT(Message.id) as messagecount,"
                    " (SELECT COUNT(DISTINCT m2.id) FROM Message AS m2"
                    "  JOIN Account AS a2 ON m2.user_id = Account.id"
                    "  WHERE m2.original_post = true) AS threadcount FROM Account "
                    " LEFT JOIN Message ON Message.user_id = Account.id  "
                    " GROUP BY Account.id;")
        return db.session.execute(stmt)

    def get_category_ids(self):
        ids = []
        for category_row in self.categories:
            ids.append(category_row.id)
        return ids


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, role):
        self.role = role
