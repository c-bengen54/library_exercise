from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db_book import *
from database.db_member import db_find, db_get_admin_code, db_update_member, db_view_logs

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html")


@admin_bp.route("/books")
def books():
    # Get all books
    return render_template("admin/books.html")


@admin_bp.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        # Read form
        # Call add_book() database function
        # Redirect

        ...

    return render_template("admin/add_book.html")


@admin_bp.route("/books/remove", methods=["GET", "POST"])
def remove_book(book_id):
    pass
