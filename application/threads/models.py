from application import db
from application.models import Base
from application.messages.models import Message
from application.auth.models import User

from sqlalchemy.sql import text

from flask_login import current_user


class Thread(Base):
    title = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False, index=True)

    messages = db.relationship("Message", backref='thread', lazy=True)

    def __init__(self, title, category_id):
        self.title = title
        self.category_id = category_id

    @staticmethod
    def get_threads(page):
        '''Return a paginated list of threads, filtered by user category and ordered by date modified'''
        return Thread.query.order_by(Thread.date_modified.desc()).filter(Thread.category_id.in_(current_user.get_category_ids())).paginate(page, 10, False)

    @staticmethod
    def get_thread(thread_id, page):
        '''Return a tuple with thread and a paginated list of messages'''
        t = Thread.query.get(thread_id)
        messages = db.session.query(Message).outerjoin(User).add_columns(User.username).filter(
            Message.thread_id == thread_id).order_by(Message.id).paginate(page, 10, False)

        return (t, messages)

    @staticmethod
    def create_thread(title, message_text, user_id, category_id):
        t = Thread(title=title, category_id=category_id)

        db.session.add(t)
        db.session.flush()
        m = Message(message_text=message_text, thread_id=t.id,
                    user_id=user_id, original_post=True)
        db.session.add(m)
        db.session.commit()

    @staticmethod
    def delete_message(message_id):
        m = Message.query.get(message_id)
        db.session.delete(m)
        db.session.commit()

    @staticmethod
    def delete_thread(thread_id):
        t = Thread.query.get(thread_id)

        stmt = Message.__table__.delete().where(Message.thread_id == t.id)
        db.engine.execute(stmt)

        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def post_reply(thread_id, message_text, user_id):
        m = Message(message_text, thread_id=thread_id,
                    user_id=user_id)

        t = Thread.query.get(thread_id)
        t.date_modified = db.func.current_timestamp()

        db.session.add(m)
        db.session.commit()
