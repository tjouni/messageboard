from flask import render_template, request, redirect, url_for

from application import app, bcrypt, db, login_required
from application.categories.models import Category
from application.categories.forms import CategoryForm, NewCategoryForm
from application.threads.models import Thread
from sqlalchemy.exc import IntegrityError


@app.route("/categories/", methods=["GET"])
@login_required("admin")
def categories_index():
    form = NewCategoryForm()
    return render_template("categories/list.html", categories=Category.get_category_list(), form=form)


@app.route("/categories/", methods=["POST"])
@login_required("admin")
def categories_create():
    form = NewCategoryForm(request.form)

    if not form.validate():
        return render_template("categories/list.html", categories=Category.get_category_list(), form=form)

    category = Category(form.name.data)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("categories/list.html", categories=Category.get_category_list(), form=form, category_name_taken=True)
    return render_template("categories/list.html", categories=Category.get_category_list(), form=form)


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
