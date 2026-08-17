from db import _execute, _fetch_one, _fetch_all

def add_book(title, author, publication, genre, isbn):
    _execute(
        """
        INSERT INTO books (title, author, publication, genre, isbn_code)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (title, author, publication, genre, isbn,)
    )

def get_book(title):
    return _fetch_one(
        """
        SELECT *
        from books
        WHERE title = %s;
        """,
        (title,)
    )

def delete_book(book_id):
    _execute(
        """
        DELETE from books
        where id = %s;
        """,
        (book_id,)
    )

def check_out(member_id, book_id):
    _execute(
        """
        UPDATE books
        SET
            checked_out = TRUE,
            holder_id = %s
        WHERE id = %s;

        INSERT INTO borrowed_books (member_id, book_id)
        VALUES (%s, %s);
        """,
        (member_id, book_id, member_id, book_id)
    )

def return_book(book_id):
    _execute(
        """
        UPDATE books
        SET 
            checked_out = FALSE,
            holder_id = NULL
        where id = %s;
        DELETE FROM borrowed_books
        where book_id = %s
        """,
        (book_id, book_id,)
    )

def reserve_book(book_id, member_id):
    _execute(
        """
        INSERT INTO reservations (book_id, member_id)
        VALUES (%s, %s);
        """,
        (book_id, member_id,)
    )

def get_reservation(book_id):
    return _fetch_all(
        """
        SELECT * 
        FROM reservations
        WHERE book_id = %s
        ORDER BY reserved_at;
        """,
        (book_id,)
    )

def cancel_reservation(book_id, member_id):
    _execute(
        """
        DELETE FROM reservations
        WHERE
            book_id = %s
        AND
            member_id = %s;
        """,
        (book_id, member_id,)
    )

def get_all_books():
    return _fetch_all(
        """
        SELECT *
        from books;
        """
        )

def is_checked_out(book_id):
    return _fetch_one(
        """
        SELECT checked_out
        from books
        where id = %s;
        """,
        (book_id,)
    )

def get_holder(book_id):
    return _fetch_one(
        """
        SELECT holder_id
        FROM books
        WHERE id = %s;
        """,
        (book_id,)
    )

book_titles = [
    "1984",
    "To Kill a Mockingbird",
    "The Hobbit",
    "Dune",
    "The Great Gatsby",
    "The Catcher in the Rye",
    "The Lord of the Rings",
    "The Martian",
    "Jurassic Park",
    "The Hunger Games",
    "The Da Vinci Code",
    "Pride and Prejudice",
    "Dracula",
    "Frankenstein",
    "The Shining",
    "Harry Potter and the Sorcerer's Stone",
    "The Name of the Wind",
    "Mistborn",
    "The Road",
    "Ready Player One"
]

authors = [
    "George Orwell",
    "Harper Lee",
    "J.R.R. Tolkien",
    "Frank Herbert",
    "F. Scott Fitzgerald",
    "J.D. Salinger",
    "J.R.R. Tolkien",
    "Andy Weir",
    "Michael Crichton",
    "Suzanne Collins",
    "Dan Brown",
    "Jane Austen",
    "Bram Stoker",
    "Mary Shelley",
    "Stephen King",
    "J.K. Rowling",
    "Patrick Rothfuss",
    "Brandon Sanderson",
    "Cormac McCarthy",
    "Ernest Cline"
]

genres = [
    "Dystopian",
    "Classic",
    "Fantasy",
    "Science Fiction",
    "Classic",
    "Classic",
    "Fantasy",
    "Science Fiction",
    "Science Fiction",
    "Young Adult",
    "Mystery",
    "Romance",
    "Horror",
    "Horror",
    "Horror",
    "Fantasy",
    "Fantasy",
    "Fantasy",
    "Post-Apocalyptic",
    "Science Fiction"
]

publication_years = [
    1949,
    1960,
    1937,
    1965,
    1925,
    1951,
    1954,
    2011,
    1990,
    2008,
    2003,
    1813,
    1897,
    1818,
    1977,
    1997,
    2007,
    2006,
    2006,
    2011
]

isbns = [
    "978-0-45-152493-5",  # 1984
    "978-0-06-093546-7",  # To Kill a Mockingbird
    "978-0-54-792822-7",  # The Hobbit
    "978-0-44-117271-9",  # Dune
    "978-0-74-327356-5",  # The Great Gatsby
    "978-0-31-676948-8",  # The Catcher in the Rye
    "978-0-61-864015-7",  # The Lord of the Rings
    "978-0-55-341802-6",  # The Martian
    "978-0-34-553898-7",  # Jurassic Park
    "978-0-43-902348-1",  # The Hunger Games
    "978-0-30-747427-8",  # The Da Vinci Code
    "978-0-14-143951-8",  # Pride and Prejudice
    "978-0-14-143984-6",  # Dracula
    "978-0-14-143947-1",  # Frankenstein
    "978-0-30-774365-7",  # The Shining
    "978-0-59-035342-7",  # Harry Potter and the Sorcerer's Stone
    "978-0-75-640474-1",  # The Name of the Wind
    "978-0-76-535038-1",  # Mistborn
    "978-0-30-738789-9",  # The Road
    "978-0-30-788744-3",  # Ready Player One
]

"""
for title, author, pub, genre, isbn in zip(book_titles, authors, publication_years, genres, isbns):
    add_book(title, author, pub, genre, isbn)
"""