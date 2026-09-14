from flask import Blueprint, render_template, request, redirect, url_for, session
from project.database.db_book import *
from project.database.db_member import db_find, db_get_admin_code, db_update_member, db_view_logs
from functools import wraps

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

@admin_bp.route("/")
@login_required
def dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route("/books/add", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        # Read form
        # Call add_book() database function
        # Redirect

        ...

    return render_template("admin_add_book.html")

@admin_bp.route("/books/remove/<int:book_id>", methods=["GET", "POST"])
@login_required
def remove_book(book_id):
    pass

@admin_bp.route("/account/update/<int:member_id>", methods=["GET", "POST"])
@login_required
def update_account(member_id):
    pass

@admin_bp.route("/logs/view", methods=["GET", "POST"])
@login_required
def view_logs():
    pass


