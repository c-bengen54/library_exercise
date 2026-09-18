from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from project.database.db_book import *
from project.database.db_member import db_find, db_update_member, db_view_logs, db_log_event
from functools import wraps
from datetime import datetime, timezone

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

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("user_type") != "admin":
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin/admin_dashboard.html")

@admin_bp.route("/books/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_book():
    if request.method == "POST":

        title = request.form["title"] 
        author = request.form["author"]
        pub = request.form["publication"]
        genre = request.form["genre"]
        isbn = request.form["isbn"]

        db_add_book(title, author, int(pub), genre, isbn)
        db_log_event(session.get("user_id"), f"Admin added book: {title}", datetime.now(timezone.utc))

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/admin_add_book.html")

@admin_bp.route("/books/remove/<int:book_id>", methods=["GET", "POST"])
@login_required
@admin_required
def remove_book(book_id):
    book = db_get_book_by("id", book_id)

    if book is None:
        abort(404)

    if request.method == "POST":
        db_delete_book(book_id)
        db_log_event(session.get("user_id"), f"Admin removed book with id: {book_id}", datetime.now(timezone.utc))

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/admin_remove_book.html", book = book)

@admin_bp.route("/account/update/<int:member_id>", methods=["GET", "POST"])
@login_required
@admin_required
def update_account(member_id):
    user = db_find("users", "user_id", member_id)

    if user is None:
        abort(404)

    if request.method == "POST":
        query = request.form["query"].strip()
        value = request.form["value"].strip()

        if query not in ("username", "user_id"):
            abort(404)

        if query == "user_id":
            try:
                value = int(value)
            except ValueError:
                abort(404)

        db_update_member(query, value, member_id)
        db_log_event(session.get("user_id"), f"Admin updated user with id: {member_id}, changed {query} to {value}", datetime.now(timezone.utc))
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/admin_update_account.html", member=user)

@admin_bp.route("/logs/view", methods=["GET", "POST"])
@login_required
@admin_required
def view_logs():
    logs = db_view_logs()
    return render_template("admin/admin_view_logs.html", logs = logs)

@admin_bp.route("/account/lookup", methods=["GET", "POST"])
@login_required
@admin_required
def lookup_account():
    if request.method == "POST":
        username = request.form["username"].strip()
        user = db_find("users", "username", username)

        if user is None:
            flash("No user found with that username.", "error")
            return redirect(url_for("admin.lookup_account"))

        return redirect(url_for("admin.update_account", member_id=user[1]))

    return render_template("admin/admin_lookup_account.html")


