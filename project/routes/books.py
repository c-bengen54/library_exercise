from flask import Blueprint, render_template, redirect, url_for, session
from functools import wraps
from project.database.db_book import (
    db_check_out,
    db_reserve_book,
    db_return_book,
    db_get_all_books,
    db_get_book_by,
    db_cancel_reservation,
    db_get_reservation
)

books_bp = Blueprint("books", __name__, url_prefix="/books")

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

@books_bp.route("/")
def books():
    books = db_get_all_books()
    return render_template("books.html", books=books)


@books_bp.route("/<int:book_id>")
@login_required
def book(book_id):
    book = db_get_book_by("id", book_id)

    if book is None:
        return "Book not found", 404

    return render_template("book.html", book=book)

@books_bp.route("/<int:book_id>/checkout", methods=["POST"])
@login_required
def checkout(book_id):
    user_id = session.get("user_id")

    db_check_out(user_id, book_id)

    return redirect(url_for("books.book", book_id=book_id))

@books_bp.route("/<int:book_id>/return", methods=["POST"])
@login_required
def return_book(book_id):
    db_return_book(book_id)
    next_holder = db_get_reservation(book_id)
    
    if next_holder:
        db_check_out(next_holder[0][2], book_id)
        db_cancel_reservation(book_id, next_holder[0][2])

    return redirect(url_for("books.book", book_id=book_id))


@books_bp.route("/<int:book_id>/reserve", methods=["POST"])
@login_required
def reserve(book_id):
    user_id=session.get("user_id")
    db_reserve_book(book_id, user_id)

    return redirect(url_for("books.book", book_id=book_id))