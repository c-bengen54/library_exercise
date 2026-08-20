from database.db import _execute, _fetch_one, _fetch_all
from psycopg import sql
import secrets
from datetime import datetime, timedelta, timezone

def db_register_member(user_id, username, firstname, lastname, email, password):
    _execute(
        """
        INSERT INTO members (user_id, username, first_name, last_name, email, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
        (user_id, username, firstname, lastname, email, password)
    )

def db_register_admin(username, admin_id):
    _execute(
        """
        INSERT INTO admins (username, admin_id)
        VALUES (%s, %s);
        """,
        (username, admin_id)
    )

def db_update_member(query, value, user_id):
    statement = sql.SQL(
        """
        UPDATE members
        SET
            {} = %s
        where user_id = %s;
        """
    ).format(
        sql.Identifier(query)
    )
    _execute(statement, (value, user_id,))

def db_find(database, query, value):
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
    _execute(
        """
        INSERT INTO logs (user_id, log_message, created_at)
        VALUES (%s, %s, %s);
        """,
        (member_id, message, timestamp)
    )

def db_view_logs():
    return _fetch_all(
        """
        SELECT * from logs;
        """
    )

def db_get_admin_code():
    return _fetch_one(
        """
        SELECT access_code, expires_at
        from admin_access
        where id = 1;
        """
    )

def db_set_admin_code(access_code:int, expiration):
    _execute(
        """
        INSERT INTO admin_access (id, access_code, expires_at)
        VALUES (1, %s, %s);
        """,
        (access_code, expiration)
    )

def db_update_admin_code(access_code:int, expiration):
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
    return secrets.randbelow(900000) + 100000

def get_next_expiration():
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