from flask import Blueprint, render_template, request, redirect, url_for, session

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