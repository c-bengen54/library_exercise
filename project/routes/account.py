from flask import Blueprint, render_template, request, redirect, url_for, session
from project.database.db_member import db_find
from project.database.db_book import db_get_book_by, db_get_reservation
from functools import wraps

account_bp = Blueprint(
    "account",
    __name__,
    url_prefix="/account"
)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


@account_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@account_bp.route("/settings")
@login_required
def settings():
    return render_template("settings.html")