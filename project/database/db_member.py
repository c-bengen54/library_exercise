from db import _execute, _fetch_one

def register_member(user_id, username, firstname, lastname, email, password):
    _execute(
        """
        INSERT INTO members (user_id, username, first_name, last_name, email, password_hash)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (user_id, username, firstname, lastname, email, password)
    )

def register_admin(username, admin_id):
    _execute(
        """
        INSERT INTO admins (username, admin_id)
        VALUES (%s, %s);
        """,
        (username, admin_id)
    )

def update_member(query, value, user_id):
    _execute(
        """
        UPDATE members
        SET
            %s = %s
        where user_id = %s;
        """,
        (query, value, user_id)
    )

def find_user(database, user_id):
    return _fetch_one(
        """
        SELECT * from %s
        where id = %s;
        """,
        (database, user_id)
    )