from flask import render_template, request, redirect, url_for

from application import app, bcrypt, db, login_required
from application.roles.models import Role
from application.roles.forms import RoleForm
from application.threads.models import Thread
from sqlalchemy.exc import IntegrityError


@app.route("/roles/", methods=["GET"])
@login_required("admin")
def roles_index():
    form = RoleForm()
    return render_template("roles/list.html", roles=Role.get_role_list(), form=form)


@app.route("/roles/", methods=["POST"])
@login_required("admin")
def roles_create():
    form = RoleForm(request.form)

    if not form.validate():
        return render_template("roles/list.html", roles=Role.get_role_list(), form=form)

    role = Role(form.name.data)
    try:
        db.session.add(role)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("roles/list.html", roles=Role.get_role_list(), form=form, Roles_name_taken=True)
    return render_template("roles/list.html", roles=Role.get_role_list(), form=form)


@app.route("/roles/<int:role_id>/", methods=["GET"])
@login_required("admin")
def roles_view(Roles_id):
    role = Role.query.get(Roles_id)
    form = RoleForm()
    return render_template("roles/view.html", role=role, form=form)


@app.route("/roles/<int:role_id>/", methods=["POST"])
@login_required("admin")
def roles_update(Roles_id):
    form = RoleForm(request.form)
    role = Role.query.get(Roles_id)

    if form.name.data:
        cat.name = form.name.data

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("roles/view.html", role=role, form=form, role_name_taken=True)
    return redirect(url_for("roles_index"))


@app.route("/roles/delete/<int:role_id>/", methods=["GET"])
@login_required("admin")
def delete_role(role_id):
    role = Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for("roles_index"))
