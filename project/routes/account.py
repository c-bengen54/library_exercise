from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db_member import db_find
from database.db_book import db_get_book_by, db_get_reservation

account_bp = Blueprint(
    "account",
    __name__,
    url_prefix="/account"
)

@account_bp.route("/dashboard")
def account():
    return render_template("dashboard.html")

@account_bp.route("/settings")
def settings():
    return render_template("settings.html")