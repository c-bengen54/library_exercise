from db import _execute, _fetch_one
from psycopg import sql

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
        INSERT INTO logs (member_id, log_message, created_at)
        VALUES (%s, %s, %s);
        """,
        (member_id, message, timestamp)
    )