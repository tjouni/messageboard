from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import User
from application.auth.forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError


@app.route("/users/", methods=["GET"])
@login_required
def auth_index():
    return render_template("auth/list.html", users=User.get_user_list())


@app.route("/auth/new/", methods=["GET"])
def auth_form():
    return render_template("auth/new.html", form=UserForm())


@app.route("/auth/new/", methods=["POST"])
def auth_create():
    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form=form)

    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    u = User(name=form.name.data, username=form.username.data,
             password=pw_hash, email=form.email.data)

    db.session.add(u)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("auth/new.html", form=form, username_taken=True)

    return redirect(url_for("auth_index"))


@app.route("/users/<int:user_id>/", methods=["POST"])
@login_required
def auth_update(user_id):
    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/view.html", user=u, form=form)

    u = User.query.get(user_id)

    if u.id == current_user.id or current_user.is_admin():
        u.username = form.username.data
        pw_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        u.password = pw_hash
        u.name = form.name.data
        u.email = form.email.data

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("auth/view.html", user=u, form=form, username_taken=True)

    return redirect(url_for("auth_index"))


@app.route("/users/<int:user_id>/", methods=["GET"])
@login_required
def auth_view(user_id):
    u = User.query.get(user_id)
    f = UserForm()
    if u.id == current_user.id or current_user.is_admin():
        return render_template("auth/view.html", user=u, form=f)

    return redirect(url_for("auth_index"))


@app.route("/users/delete/<int:user_id>/", methods=["GET"])
@login_required
def delete_user(user_id):
    u = User.query.get(user_id)

    if u.id == current_user.id or current_user.is_admin():
        db.session.delete(u)
        db.session.commit()

    return redirect(url_for("auth_index"))


@app.route("/auth/", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    user = User.query.filter_by(username=form.username.data).first()

    if not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form,
                               error="Incorrect username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
