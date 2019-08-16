from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import AddUserForm, LoginForm


@app.route("/auth/login/", methods=["GET"])
@login_required
def auth_index():
    return render_template("auth/list.html", users=User.get_user_list())


@app.route("/auth/new/", methods=["GET"])
@login_required
def auth_form():
    return render_template("auth/new.html", form=AddUserForm())


@app.route("/auth/new/", methods=["POST"])
@login_required
def auth_create():
    form = AddUserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form=form)

    u = User(name=form.name.data, username=form.username.data,
             password=form.password.data, email=form.email.data)

    db.session.add(u)
    db.session.commit()

    return render_template("auth/new.html", form=AddUserForm())


@app.route("/auth/", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
                               error="Incorrect username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
