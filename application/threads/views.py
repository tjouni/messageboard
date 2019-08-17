from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.threads.models import Thread
from application.threads.forms import ThreadForm

from application.messages.models import Message
from application.messages.forms import MessageForm


@app.route("/threads/", methods=["GET"])
@login_required
def threads_index():
    return render_template("threads/list.html", threads=Thread.get_threads())


@app.route("/threads/new/", methods=["GET"])
@login_required
def threads_form():
    return render_template("threads/new.html", form=ThreadForm())


@app.route("/threads/", methods=["POST"])
@login_required
def threads_create():
    form = ThreadForm(request.form)

    if not form.validate():
        return render_template("threads/new.html", form=form)

    Thread.create_thread(
        title=form.title.data, message_text=form.message_text.data, user_id=current_user.id)

    return redirect(url_for("threads_index"))


@app.route("/threads/<int:thread_id>/", methods=["GET"])
@login_required
def threads_view(thread_id, form=None):
    if form is None:
        form = MessageForm(request.form)

    (t, res) = Thread.get_thread(thread_id)

    return render_template("threads/view.html", thread=t, messages=res, form=form)


@app.route("/delete/<int:message_id>/", methods=["GET"])
@login_required
def delete_message(message_id, form=None):
    if form is None:
        form = MessageForm(request.form)

    m = Message.query.get(message_id)
    if m.original_post:
        Thread.delete_thread(m.thread_id)
        return redirect(url_for("threads_index"))

    Thread.delete_message(message_id)
    (t, res) = Thread.get_thread(m.thread_id)

    return render_template("threads/view.html", thread=t, messages=res, form=form)


@app.route("/threads/<int:thread_id>/", methods=["POST"])
@login_required
def threads_reply(thread_id):
    form = MessageForm(request.form)

    if not form.validate():
        return threads_view(thread_id, form=form)

    Thread.post_reply(thread_id=thread_id,
                      message_text=form.message_text.data, user_id=current_user.id)

    return redirect(url_for("threads_view", thread_id=thread_id))
