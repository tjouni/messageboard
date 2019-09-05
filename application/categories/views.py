from flask import render_template, request, redirect, url_for

from application import app, bcrypt, db, login_required
from application.categories.models import Category
from application.threads.models import Thread


@app.route("/categories/", methods=["GET"])
@login_required("admin")
def categories_index():
    return render_template("categories/list.html", categories=Category.get_category_list())


@app.route("/categories/new/", methods=["GET"])
@login_required("admin")
def categories_create():
    return None


@app.route("/categories/delete/<int:category_id>/", methods=["GET"])
@login_required("admin")
def delete_category(category_id):
    cat = Category.query.get(category_id)
    threads = db.session.query(Thread).filter(
        Thread.category_id == category_id)
    for thread in threads:
        Thread.delete_thread(thread.id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for("categories_index"))
