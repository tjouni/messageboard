from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from application import app, bcrypt, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, NewUserForm, UpdateUserForm
from application.categories.models import Category
from sqlalchemy.exc import IntegrityError


@app.route("/users/", methods=["GET"])
@login_required()
def auth_index():
    return render_template("auth/list.html", users=User.get_user_list())


@app.route("/auth/new/", methods=["GET"])
def auth_form():
    return render_template("auth/new.html", form=NewUserForm())


@app.route("/auth/new/", methods=["POST"])
def auth_create():
    form = NewUserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form=form)

    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    u = User(name=form.name.data, username=form.username.data,
             password=pw_hash, email=form.email.data)

    db.session.add(u)

    try:
        default_category = db.session.query(Category).get(1)
        u.categories.append(default_category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("auth/new.html", form=form, username_taken=True)

    return redirect(url_for("auth_index"))


@app.route("/users/<int:user_id>/", methods=["POST"])
@login_required()
def auth_update(user_id):
    form = UpdateUserForm(request.form)
    u = User.query.get(user_id)

    if not form.validate():
        return render_template("auth/view.html", user=u, form=form)

    if u.id == current_user.id or current_user.is_admin():
        if form.username.data:
            u.username = form.username.data
        if form.new_password.data:
            if form.new_password.data != form.repeat_password.data:
                form.repeat_password.errors.append('Passwords do not match')
                return render_template("auth/view.html", user=u, form=form)
            pw_hash = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            u.password = pw_hash
        if form.name.data:
            u.name = form.name.data
        if form.email.data:
            u.email = form.email.data
        u.roles = form.role.data
        u.categories = form.category.data

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("auth/view.html", user=u, form=form, username_taken=True)

    return redirect(url_for("auth_index"))


@app.route("/users/<int:user_id>/", methods=["GET"])
@login_required()
def auth_view(user_id):
    u = User.query.get(user_id)
    form = UpdateUserForm(request.form)
    if u.id == current_user.id or current_user.is_admin():
        return render_template("auth/view.html", user=u, form=form)

    return redirect(url_for("auth_index"))


@app.route("/users/delete/<int:user_id>/", methods=["GET"])
@login_required()
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

    if not user or not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form,
                               error="Incorrect username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
