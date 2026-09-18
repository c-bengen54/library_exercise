from flask import Blueprint, render_template, request, redirect, url_for, session
from project.database.db_member import * 
import bcrypt, random, pyotp, os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

ADMIN_TOTP = pyotp.TOTP(os.getenv("ADMIN_TOTP_SECRET"))

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        identity = int(request.form["user_id"])

        user = db_find("users", "user_id", identity)

        if user is None:
            return render_template(
                "system/login.html",
                error="Invalid login information."
            )

        if user[2] != username:
            return render_template(
                "system/login.html",
                error="Invalid login information."
            )

        password = password.encode("utf-8")
        stored_hash = bytes.fromhex(user[6][2:])

        if not bcrypt.checkpw(password, stored_hash):
            return render_template(
                "system/login.html",
                error="Invalid login information."
            )

        session["user_id"] = user[1]
        session["username"] = user[2]
        session["first_name"] = user[3]
        session["last_name"] = user[4]
        session["email"] = user[5]
        session["user_type"] = user[7]

        db_log_event(user[1], f"User with id: {user[1]} logged in", datetime.now(timezone.utc))

        if user[7] == "admin":
            return redirect(url_for("admin.dashboard"))
        
        return redirect(url_for("account.dashboard"))

    return render_template("system/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt()).strip()
        email = request.form["email"].strip()
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        access_code = request.form["access_code"].strip()

        while True:
                    identity = random.randint(100000, 999999)
                    if db_find("users", "user_id", identity) is None:
                        break
        
        if not ADMIN_TOTP.verify(access_code, valid_window=1):
            user_type = "member"
        else:
            user_type = "admin"

        session["user_id"] = identity
        session["username"] = username
        session["first_name"] = first_name
        session["last_name"] = last_name
        session["email"] = email
        session["user_type"] = user_type

        db_register_user(identity, username, first_name, last_name, email, password, user_type)

        db_log_event(identity, f"User registered with type: {user_type}", datetime.now(timezone.utc))

        if user_type == "admin":
             return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("account.dashboard"))

    return render_template("system/register.html")

@auth_bp.route("/logout")
def logout():
    db_log_event(session.get("user_id"), f"User with id {session.get("user_id")} has logged out", datetime.now(timezone.utc))
    session.clear()

    return redirect(url_for("auth.login"))