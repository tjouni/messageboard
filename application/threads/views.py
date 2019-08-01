from application import app, db
from flask import redirect, render_template, request, url_for
from application.threads.models import Thread
from application.messages.models import Message
from sqlalchemy.sql import text


@app.route("/threads/", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads=Thread.query.all())


@app.route("/threads/new/")
def threads_form():
    return render_template("threads/new.html")


@app.route("/threads/", methods=["POST"])
def threads_create():
    t = Thread(request.form.get("title"))

    db.session.add(t)
    db.session.flush()

    m = Message(message_text=request.form.get("message_text"), thread_id=t.id)

    db.session.add(m)
    db.session.commit()

    return redirect(url_for("threads_index"))


@app.route("/threads/<int:thread_id>/", methods=["GET"])
def threads_view(thread_id):
    t = Thread.query.get(thread_id)

    stmt = text("SELECT id, date_created, message_text FROM Message"
                " WHERE thread_id = :tid").params(tid=t.id)

    res = db.engine.execute(stmt)
    db.session.commit()

    return render_template("threads/view.html", thread=t, messages=res)


@app.route("/threads/<int:thread_id>/", methods=["POST"])
def threads_reply(thread_id):
    m = Message(message_text=request.form.get(
        "message_text"), thread_id=thread_id)

    db.session.add(m)
    db.session.commit()

    return redirect(url_for("threads_view", thread_id=thread_id))
