from flask import render_template, request, redirect, url_for

from application import app, bcrypt, db, login_required
from application.categories.models import Category


@app.route("/categories/", methods=["GET"])
@login_required("admin")
def categories_index():
    return render_template("categories/list.html", categories=Category.get_category_list())


@app.route("/categories/new/", methods=["GET"])
@login_required("admin")
def categories_create():
    return None


@app.route("/categoriess/delete/<int:category_id>/", methods=["GET"])
@login_required("admin")
def delete_category(category_id):
    u = Category.query.get(category_id)

    return redirect(url_for("auth_index"))
