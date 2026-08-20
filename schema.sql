CREATE OR REPLACE FUNCTION fn_isbn(isbn TEXT) 
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    clean_isbn TEXT;
    total INTEGER:= 0;
    i INTEGER;
    digit INTEGER;
BEGIN

    clean_isbn:=REPLACE(UPPER(isbn), '-', '');


    IF clean_isbn ~ '^[0-9]{9}[0-9X]$' THEN
        FOR i in 1..10 LOOP

            IF i = 10 AND SUBSTRING(clean_isbn, i, 1) = 'X' THEN
                digit := 10;
            ELSE
                digit:= SUBSTRING(clean_isbn, i, 1)::INTEGER;
            END IF;

            total:= total + digit * (11-i);
        END LOOP;

        IF total % 11 = 0 THEN
            RETURN TRUE;
        ELSE
            RETURN FALSE;
        END IF;
        

    ELSIF clean_isbn ~ '^[0-9]{13}$' THEN
        FOR i in 1..13 LOOP
            digit:=SUBSTRING(clean_isbn, i, 1)::INTEGER;
            IF i % 2 = 1 THEN
                total:= total + digit;
            ELSIF i % 2 = 0 THEN
                total:= total + digit * 3;
            END IF;
        END LOOP;

        IF total % 10 = 0 THEN
            RETURN TRUE;
        ELSE
            RETURN FALSE;
        END IF;

    ELSE
        RETURN FALSE;

    END IF;
END;
$$;

CREATE TABLE IF NOT EXISTS members (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    admin_id INTEGER UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES members(user_id),
    log_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication INTEGER,
    genre TEXT,
    isbn_code VARCHAR(17) UNIQUE NOT NULL,
    checked_out BOOLEAN DEFAULT FALSE,
    holder_id INTEGER REFERENCES members(user_id),
    CONSTRAINT check_isbn CHECK(fn_isbn(isbn_code))
);

CREATE TABLE IF NOT EXISTS borrowed_books (
    member_id INTEGER REFERENCES members(user_id),
    book_id INTEGER REFERENCES books(id),
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(member_id, book_id)
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    book_id INTEGER NOT NULL
        REFERENCES books(id),

    member_id INTEGER NOT NULL
        REFERENCES members(user_id),

    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(book_id, member_id)
);

CREATE TABLE IF NOT EXISTS admin_access (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    access_code INTEGER NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL
);