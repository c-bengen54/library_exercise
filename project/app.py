from flask import Flask
import os
from dotenv import load_dotenv
from pathlib import Path

from routes.main import main_bp
from routes.books import books_bp
from routes.auth import auth_bp
from routes.account import account_bp
from routes.admin import admin_bp


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