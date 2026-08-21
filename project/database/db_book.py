from database.db import _execute, _fetch_one, _fetch_all
from psycopg import sql

def db_add_book(title, author, publication, genre, isbn):
    """
    Adds a new book to the books table.

    Parameters:
        title (str):
            Title of the book.
        author (str):
            Author of the book.
        publication (int):
            Year the book was published.
        genre (str):
            Genre or category of the book.
        isbn (str):
            ISBN-10 or ISBN-13 identifier for the book. Hyphens may be
            accepted depending on the database validation function.

    Returns:
        None
    """
    _execute(
        """
        INSERT INTO books (title, author, publication, genre, isbn_code)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (title, author, publication, genre, isbn,)
    )

def db_get_book_by(query, param):
    """
    Finds the first book matching a specified column and value.

    Parameters:
        query (str):
            Name of the books table column to search.
            Examples include "id", "title", "author", or "isbn_code".
        param:
            Value to search for. Its type must match the selected column.

    Returns:
        tuple | None:
            The first matching book record, or None if no matching book
            is found.
    """
    statement = sql.SQL(
        """
        SELECT *
        from books
        WHERE {} = %s
        """
    ).format(
        sql.Identifier(query)
    )
    return _fetch_one(statement, (param,))

def db_delete_book(book_id):
    """
    Deletes a book from the books table.

    Parameters:
        book_id (int):
            Unique database ID of the book to delete.

    Returns:
        None
    """
    _execute(
        """
        DELETE from books
        where id = %s;
        """,
        (book_id,)
    )

def db_check_out(member_id, book_id):
    """
    Checks a book out to a member.

    This updates the book's checkout status and holder ID and creates a
    corresponding record in the borrowed_books table.

    Parameters:
        member_id (int):
            Unique ID of the member borrowing the book.
        book_id (int):
            Unique ID of the book being checked out.

    Returns:
        None
    """
    _execute(
        """
        BEGIN TRANSACTION;

        UPDATE books
        SET
            checked_out = TRUE,
            holder_id = %s
        WHERE id = %s;

        INSERT INTO borrowed_books (member_id, book_id)
        VALUES (%s, %s);

        COMMIT;
        """,
        (member_id, book_id, member_id, book_id)
    )

def db_return_book(book_id):
    """
    Marks a book as returned and removes its borrowed_books record.

    Parameters:
        book_id (int):
            Unique ID of the book being returned.

    Returns:
        None
    """
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

def db_reserve_book(book_id, member_id):
    """
    Adds a member to the reservation queue for a book.

    Parameters:
        book_id (int):
            Unique ID of the book being reserved.
        member_id (int):
            Unique ID of the member making the reservation.

    Returns:
        None
    """
    _execute(
        """
        INSERT INTO reservations (book_id, member_id)
        VALUES (%s, %s);
        """,
        (book_id, member_id,)
    )

def db_get_reservation(book_id):
    """
    Retrieves all reservations for a specific book in the order they
    were created.

    Parameters:
        book_id (int):
            Unique ID of the book whose reservation queue is being
            retrieved.

    Returns:
        list:
            List of reservation records ordered by reservation time.
    """
    return _fetch_all(
        """
        SELECT * 
        FROM reservations
        WHERE book_id = %s
        ORDER BY reserved_at;
        """,
        (book_id,)
    )

def db_cancel_reservation(book_id, member_id):
    """
    Removes a member's reservation for a specific book.

    Parameters:
        book_id (int):
            Unique ID of the reserved book.
        member_id (int):
            Unique ID of the member whose reservation should be removed.

    Returns:
        None
    """
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

def db_get_all_books():
    """
    Retrieves all books that are currently available for checkout.

    Returns only books whose checked_out value is FALSE.

    Parameters:
        None

    Returns:
        list:
            List of available book records.
    """
    return _fetch_all(
        """
        SELECT *
        from books
        WHERE checked_out = FALSE;
        """
        )

def db_is_checked_out(book_id):
    """
    Determines whether a specific book is currently checked out.

    Parameters:
        book_id (int):
            Unique ID of the book to check.

    Returns:
        tuple | None:
            A tuple containing the book's checked_out value, or None if
            the book does not exist.
    """
    return _fetch_one(
        """
        SELECT checked_out
        from books
        where id = %s;
        """,
        (book_id,)
    )

def db_get_holder(book_id):
    """
    Retrieves the ID of the member currently holding a book.

    Parameters:
        book_id (int):
            Unique ID of the book.

    Returns:
        tuple | None:
            A tuple containing the holder's member ID, or None if the
            book does not exist or currently has no holder.
    """
    return _fetch_one(
        """
        SELECT holder_id
        FROM books
        WHERE id = %s;
        """,
        (book_id,)
    )