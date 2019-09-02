from flask import redirect, render_template, request, url_for
from flask_login import current_user
from flask_paginate import Pagination, get_page_parameter

from application import app, db, login_required, login_manager
from application.threads.models import Thread
from application.threads.forms import ThreadForm

from application.messages.models import Message
from application.messages.forms import MessageForm


@app.route("/threads/", methods=["GET"])
@login_required()
def threads_index():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    threads = Thread.get_threads(page)

    pagination = Pagination(page=page, total=threads.total,
                            search=search, record_name='threads', css_framework='bootstrap4')
    return render_template("threads/list.html", threads=threads.items, pagination=pagination)


@app.route("/threads/new/", methods=["GET"])
@login_required()
def threads_form():
    return render_template("threads/new.html", form=ThreadForm())


@app.route("/threads/", methods=["POST"])
@login_required()
def threads_create():
    form = ThreadForm(request.form)

    if not form.validate():
        return render_template("threads/new.html", form=form)

    Thread.create_thread(
        title=form.title.data, message_text=form.message_text.data, user_id=current_user.id)

    return redirect(url_for("threads_index"))


@app.route("/threads/<int:thread_id>/", methods=["GET"])
@login_required()
def threads_view(thread_id, form=None):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    if form is None:
        form = MessageForm(request.form)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    (t, messages) = Thread.get_thread(thread_id, page)

    pagination = Pagination(page=page, total=messages.total,
                            search=search, record_name='messages', css_framework='bootstrap4')

    return render_template("threads/view.html", thread=t, messages=messages.items, form=form, pagination=pagination)


@app.route("/delete/<int:message_id>/", methods=["GET"])
@login_required()
def delete_message(message_id, form=None):
    if form is None:
        form = MessageForm(request.form)

    m = Message.query.get(message_id)
    u = current_user

    if m.user_id != u.id and not u.is_admin():
        return redirect(url_for("threads_view", thread_id=m.thread_id))

    if m.original_post:
        Thread.delete_thread(m.thread_id)
        return redirect(url_for("threads_index"))

    Thread.delete_message(message_id)
    (t, res) = Thread.get_thread(m.thread_id)

    return render_template("threads/view.html", thread=t, messages=res, form=form)


@app.route("/message/<int:message_id>/", methods=["GET"])
@login_required()
def message_view(message_id):
    m = Message.query.get(message_id)
    u = current_user

    if m.user_id != u.id and not u.is_admin():
        return redirect(url_for("threads_view", thread_id=m.thread_id))

    f = MessageForm()
    f.message_text.data = m.message_text
    return render_template("threads/edit.html", message=m, form=f)


@app.route("/message/update/<int:message_id>/", methods=["POST"])
@login_required()
def message_update(message_id):
    form = MessageForm(request.form)
    m = Message.query.get(message_id)
    u = current_user

    if m.user_id != u.id and not u.is_admin():
        return redirect(url_for("threads_view", thread_id=m.thread_id))

    if not form.validate():
        return render_template("threads/edit.html", message=m, form=form)

    m.message_text = form.message_text.data

    db.session.commit()

    return redirect(url_for("threads_view", thread_id=m.thread_id))


@app.route("/threads/<int:thread_id>/", methods=["POST"])
@login_required()
def threads_reply(thread_id):
    form = MessageForm(request.form)

    if not form.validate():
        return threads_view(thread_id, form=form)

    Thread.post_reply(thread_id=thread_id,
                      message_text=form.message_text.data, user_id=current_user.id)

    return redirect(url_for("threads_view", thread_id=thread_id))
