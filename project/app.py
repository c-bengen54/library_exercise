from flask import Flask
from dotenv import load_dotenv
import os
from pathlib import Path

from project.routes.app_main import main_bp
from project.routes.books import books_bp
from project.routes.auth import auth_bp
from project.routes.account import account_bp
from project.routes.admin import admin_bp


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(main_bp)
app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    app.run(debug=True)