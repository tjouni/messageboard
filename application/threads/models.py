from application import db
from application.models import Base
from application.messages.models import Message


from sqlalchemy.sql import text


class Thread(Base):
    title = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False, index=True)

    messages = db.relationship("Message", backref='thread', lazy=True)

    def __init__(self, title, category_id):
        self.title = title
        self.category_id = 0  # TODO

    @staticmethod
    def get_threads(page):
        '''Return a paginated list of threads ordered by date modified'''
        return Thread.query.order_by(Thread.date_modified.desc()).paginate(page, 10, False)

    @staticmethod
    def get_thread(thread_id):
        '''Return a tuple with thread and a paginated list of messages'''
        t = Thread.query.get(thread_id)

        stmt = text("SELECT Message.id, Message.date_created, Message.date_modified,"
                    " message_text, user_id, username FROM Message"
                    " LEFT JOIN Account ON Message.user_id = Account.id"
                    " WHERE thread_id = :tid"
                    " ORDER BY Message.id ASC").params(tid=t.id)

        res = db.session.execute(stmt).fetchall()

        return (t, res)

    @staticmethod
    def create_thread(title, message_text, user_id):
        t = Thread(title=title, category_id=0)

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
