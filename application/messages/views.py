from application import app, db
from flask import redirect, render_template, request, url_for
from application.messages.models import Message


@app.route("/messages", methods=["GET"])
def messages_index():
    return render_template("messages/list.html", messages=Message.query.all())


@app.route("/messages/new/")
def messsages_form():
    return render_template("messages/new.html")


@app.route("/messages/", methods=["POST"])
def messages_create():
    m = Message(request.form.get("message_text"))

    db.session.add(m)
    db.session.commit()

    return redirect(url_for("messages_index"))
