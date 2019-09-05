from flask import render_template, request, redirect, url_for

from application import app, bcrypt, db, login_required
from application.categories.models import Category
from application.categories.forms import CategoryForm
from application.threads.models import Thread
from sqlalchemy.exc import IntegrityError


@app.route("/categories/", methods=["GET"])
@login_required("admin")
def categories_index():
    return render_template("categories/list.html", categories=Category.get_category_list())


@app.route("/categories/new/", methods=["GET"])
@login_required("admin")
def categories_create():
    return None


@app.route("/categories/<int:category_id>/", methods=["GET"])
@login_required("admin")
def categories_view(category_id):
    cat = Category.query.get(category_id)
    form = CategoryForm()
    return render_template("categories/view.html", category=cat, form=form)


@app.route("/categories/<int:category_id>/", methods=["POST"])
@login_required("admin")
def categories_update(category_id):
    form = CategoryForm(request.form)
    cat = Category.query.get(category_id)

    if form.name.data:
        cat.name = form.name.data

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("categories/view.html", category=cat, form=form, category_name_taken=True)
    return redirect(url_for("categories_index"))


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
