from database.db import _execute, _fetch_one, _fetch_all
from psycopg import sql
import secrets
from datetime import datetime, timedelta, timezone

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

def db_get_admin_code():
    """
    Retrieves the currently active administrator access code and its
    expiration time.

    Parameters:
        None

    Returns:
        tuple | None:
            A tuple containing the access code and expiration timestamp,
            or None if no administrator access code has been created.
    """
    return _fetch_one(
        """
        SELECT access_code, expires_at
        from admin_access
        where id = 1;
        """
    )

def db_set_admin_code(access_code:int, expiration):
    """
    Creates the initial administrator access code in the database.

    Parameters:
        access_code (int):
            Six-digit numeric administrator access code.
        expiration (datetime):
            Time at which the access code expires. Should be a
            timezone-aware datetime object.

    Returns:
        None
    """
    _execute(
        """
        INSERT INTO admin_access (id, access_code, expires_at)
        VALUES (1, %s, %s);
        """,
        (access_code, expiration)
    )

def db_update_admin_code(access_code:int, expiration:datetime):
    """
    Replaces the current administrator access code with a new code and
    expiration time.

    Parameters:
        access_code (int):
            New six-digit numeric administrator access code.
        expiration (datetime):
            New expiration time for the access code. Should be a
            timezone-aware datetime object.

    Returns:
        None
    """
    _execute(
        """
        UPDATE admin_access
        SET 
            access_code = %s,
            expires_at = %s
        WHERE id = 1;
        """,
        (access_code, expiration)
    )

CODE_INTERVAL = 30

def gen_admin_code():
    """
    Generates a cryptographically secure six-digit administrator access
    code.

    Parameters:
        None

    Returns:
        int:
            A randomly generated six-digit integer between 100000 and
            999999.
    """
    return secrets.randbelow(900000) + 100000

def get_next_expiration():
    """
    Calculates the next expiration time for an administrator access code.

    The expiration is aligned with the configured CODE_INTERVAL. For
    example, with a 30-minute interval, codes expire at :00 or :30.

    Parameters:
        None

    Returns:
        datetime:
            A timezone-aware UTC datetime representing the next expiration
            time.
    """
    now = datetime.now(timezone.utc)
    minute = now.minute
    next_minute = ((minute//CODE_INTERVAL)+1)*CODE_INTERVAL

    if next_minute >= 60:
        expiration = now.replace(
            minute=0,
            second=0,
            microsecond=0
        ) + timedelta(hours=1)
    else:
        expiration = now.replace(
            minute=next_minute,
            second=0,
            microsecond=0
        )

    return expiration

def initialize_admin_code():
    """
    Retrieves and, if necessary, generates the current administrator
    access code.

    If no access code exists, a new code is created. If the existing code
    has expired, a new code and expiration time are generated.

    Parameters:
        None

    Returns:
        tuple:
            A tuple containing the current six-digit access code and its
            expiration datetime.
    """
    result = db_get_admin_code()

    if result == None:
        code = gen_admin_code()
        expiration = get_next_expiration()
        db_set_admin_code(code, expiration)
        return code, expiration

    code, expiration = result

    if datetime.now(timezone.utc) >= expiration:
        code = gen_admin_code()
        expiration = get_next_expiration()
        db_update_admin_code(code, expiration)

    return code, expiration