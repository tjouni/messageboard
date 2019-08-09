from application import app, db
from flask import redirect, render_template, request, url_for
from application.threads.models import Thread
from application.threads.forms import ThreadForm

from application.messages.models import Message
from application.messages.forms import MessageForm
from sqlalchemy.sql import text


@app.route("/threads/", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads=Thread.query.all())


@app.route("/threads/new/")
def threads_form():
    return render_template("threads/new.html", form=ThreadForm())


@app.route("/threads/", methods=["POST"])
def threads_create():
    form = ThreadForm(request.form)

    if not form.validate():
        return render_template("threads/new.html", form=form)

    t = Thread(form.title.data)

    db.session.add(t)
    db.session.flush()

    m = Message(form.message_text.data, thread_id=t.id)

    db.session.add(m)
    db.session.commit()

    return redirect(url_for("threads_index"))


@app.route("/threads/<int:thread_id>/", methods=["GET"])
def threads_view(thread_id, form=None):
    if form is None:
        form = MessageForm(request.form)

    t = Thread.query.get(thread_id)

    stmt = text("SELECT id, date_created, message_text FROM Message"
                " WHERE thread_id = :tid").params(tid=t.id)

    res = db.engine.execute(stmt)
    db.session.commit()

    return render_template("threads/view.html", thread=t, messages=res, form=form)


@app.route("/threads/<int:thread_id>/", methods=["POST"])
def threads_reply(thread_id):
    form = MessageForm(request.form)

    if not form.validate():
        return threads_view(thread_id, form=form)

    m = Message(form.message_text.data, thread_id=thread_id)

    t = Thread.query.get(thread_id)
    t.date_modified = db.func.current_timestamp()

    db.session.add(m)
    db.session.commit()

    return redirect(url_for("threads_view", thread_id=thread_id))
