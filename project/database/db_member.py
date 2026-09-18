from project.database.db import _execute, _fetch_one, _fetch_all
from psycopg import sql

def db_register_user(user_id, username, firstname, lastname, email, password, user_type):
    """
    Registers a new user in the users table.

    Parameters:
        user_id (int):
            Unique numeric ID assigned to the user.
        username (str):
            Username the user will use to identify themselves.
        firstname (str):
            User's first name.
        lastname (str):
            User's last name.
        email (str):
            User's email address.
        password (bytes):
            Password hash for the user's account. This should not be
            stored as plain-text.
        user_type (str):
            Type of user being registered, such as "member" or "admin".

    Returns:
        None
    """
    _execute(
        """
        INSERT INTO users (user_id, username, first_name, last_name, email, password_hash, user_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        (user_id, username, firstname, lastname, email, password, user_type)
    )

def db_update_member(query, value, user_id):
    """
    Updates a specific column for an existing user.

    Parameters:
        query (str):
            Name of the users table column to update. This must be a
            valid column name.
        value:
            New value to assign to the specified column. The type should
            match the column being updated.
        user_id (int):
            Unique ID of the user whose information will be updated.

    Returns:
        None
    """
    statement = sql.SQL(
        """
        UPDATE users
        SET
            {} = %s
        where user_id = %s;
        """
    ).format(
        sql.Identifier(query)
    )
    _execute(statement, (value, user_id,))

def db_find(database, query, value):
    """
    Finds the first database record matching a specified column and value.

    Parameters:
        database (str):
            Name of the database table to search.
        query (str):
            Name of the column to search.
        value:
            Value to search for. The type should match the specified
            column.

    Returns:
        tuple | None:
            The first matching database record as a tuple, or None if
            no matching record is found.
    """
    statement = sql.SQL(
        """
        SELECT * from {}
        where {} = %s;
        """
    ).format(
        sql.Identifier(database),
        sql.Identifier(query)
    )
    return _fetch_one(statement, (value,))

def db_log_event(member_id, message, timestamp):
    """
    Adds an event to the system log.

    Parameters:
        member_id (int):
            ID of the user associated with the event.
        message (str):
            Description of the event being logged.
        timestamp (datetime):
            Date and time when the event occurred. Preferably a timezone-
            aware datetime object.

    Returns:
        None
    """
    _execute(
        """
        INSERT INTO logs (user_id, log_message, created_at)
        VALUES (%s, %s, %s);
        """,
        (member_id, message, timestamp)
    )

def db_view_logs():
    """
    Retrieves all events stored in the system log.

    Parameters:
        None

    Returns:
        list:
            A list containing all log records from the logs table.
    """
    return _fetch_all(
        """
        SELECT * from logs;
        """
    )