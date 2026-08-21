-- ============================================================
-- Library Management System - Sample Data
-- ============================================================
-- This file is intended for development/testing only.
-- The password_hash values are fake placeholder values.

INSERT INTO users
    (user_id, username, first_name, last_name, email, password_hash, user_type)
VALUES
    (1001, 'jdoe',       'John',       'Doe',       'jdoe@example.com',       'sample_hash_1001', 'member'),
    (1002, 'asmith',     'Alice',      'Smith',     'asmith@example.com',     'sample_hash_1002', 'member'),
    (1003, 'bjohnson',   'Bob',        'Johnson',   'bjohnson@example.com',   'sample_hash_1003', 'member'),
    (1004, 'cwilliams',  'Charlie',    'Williams',  'cwilliams@example.com',  'sample_hash_1004', 'member'),
    (1005, 'dgarcia',    'David',      'Garcia',    'dgarcia@example.com',    'sample_hash_1005', 'member'),
    (1006, 'emartinez',  'Emma',       'Martinez',  'emartinez@example.com',  'sample_hash_1006', 'member'),
    (1007, 'flee',       'Frank',      'Lee',       'flee@example.com',        'sample_hash_1007', 'member'),
    (1008, 'gthompson',  'Grace',      'Thompson',  'gthompson@example.com',   'sample_hash_1008', 'member'),

    (2001, 'admin1',     'James',      'Wilson',    'admin1@example.com',     'sample_hash_2001', 'admin'),
    (2002, 'admin2',     'Sarah',      'Brown',     'admin2@example.com',     'sample_hash_2002', 'admin');

INSERT INTO books
    (title, author, publication, genre, isbn_code, checked_out, holder_id)
VALUES
    (
        'The Great Gatsby',
        'F. Scott Fitzgerald',
        1925,
        'Classic',
        '9780743273565',
        FALSE,
        NULL
    ),

    (
        '1984',
        'George Orwell',
        1949,
        'Dystopian',
        '9780451524935',
        TRUE,
        1001
    ),

    (
        'The Hobbit',
        'J.R.R. Tolkien',
        1937,
        'Fantasy',
        '9780547928227',
        TRUE,
        1002
    ),

    (
        'Dune',
        'Frank Herbert',
        1965,
        'Science Fiction',
        '9780441172719',
        FALSE,
        NULL
    ),

    (
        'To Kill a Mockingbird',
        'Harper Lee',
        1960,
        'Classic',
        '9780061120084',
        TRUE,
        1003
    ),

    (
        'The Catcher in the Rye',
        'J.D. Salinger',
        1951,
        'Classic',
        '9780316769488',
        FALSE,
        NULL
    ),

    (
        'The Martian',
        'Andy Weir',
        2011,
        'Science Fiction',
        '9780804139021',
        TRUE,
        1004
    ),

    (
        'Jurassic Park',
        'Michael Crichton',
        1990,
        'Science Fiction',
        '9780345538987',
        FALSE,
        NULL
    ),

    (
        'The Hunger Games',
        'Suzanne Collins',
        2008,
        'Young Adult',
        '9780439023481',
        TRUE,
        1005
    ),

    (
        'Pride and Prejudice',
        'Jane Austen',
        1813,
        'Romance',
        '9780141439518',
        FALSE,
        NULL
    ),

    (
        'Dracula',
        'Bram Stoker',
        1897,
        'Horror',
        '9780486411095',
        FALSE,
        NULL
    ),

    (
        'Frankenstein',
        'Mary Shelley',
        1818,
        'Horror',
        '9780486282114',
        TRUE,
        1006
    ),

    (
        'The Shining',
        'Stephen King',
        1977,
        'Horror',
        '9780307743657',
        FALSE,
        NULL
    ),

    (
        'Ready Player One',
        'Ernest Cline',
        2011,
        'Science Fiction',
        '9780307887443',
        TRUE,
        1007
    ),

    (
        'The Road',
        'Cormac McCarthy',
        2006,
        'Post-Apocalyptic',
        '9780307386458',
        FALSE,
        NULL
    );

INSERT INTO borrowed_books
    (member_id, book_id, borrowed_at)
VALUES
    (1001, 2, CURRENT_TIMESTAMP - INTERVAL '5 days'),
    (1002, 3, CURRENT_TIMESTAMP - INTERVAL '3 days'),
    (1003, 5, CURRENT_TIMESTAMP - INTERVAL '7 days'),
    (1004, 7, CURRENT_TIMESTAMP - INTERVAL '2 days'),
    (1005, 9, CURRENT_TIMESTAMP - INTERVAL '10 days'),
    (1006, 12, CURRENT_TIMESTAMP - INTERVAL '4 days'),
    (1007, 14, CURRENT_TIMESTAMP - INTERVAL '1 day');

INSERT INTO reservations
    (book_id, member_id, reserved_at)
VALUES
    (2, 1008, CURRENT_TIMESTAMP - INTERVAL '2 days'),
    (2, 1006, CURRENT_TIMESTAMP - INTERVAL '1 day'),

    (3, 1003, CURRENT_TIMESTAMP - INTERVAL '4 days'),

    (5, 1007, CURRENT_TIMESTAMP - INTERVAL '3 days'),

    (7, 1001, CURRENT_TIMESTAMP - INTERVAL '1 day'),

    (9, 1008, CURRENT_TIMESTAMP - INTERVAL '6 hours');

INSERT INTO logs
    (user_id, log_message, created_at)
VALUES
    (1001, 'Checked out "1984".',
        CURRENT_TIMESTAMP - INTERVAL '5 days'),

    (1002, 'Checked out "The Hobbit".',
        CURRENT_TIMESTAMP - INTERVAL '3 days'),

    (1003, 'Checked out "To Kill a Mockingbird".',
        CURRENT_TIMESTAMP - INTERVAL '7 days'),

    (1004, 'Checked out "The Martian".',
        CURRENT_TIMESTAMP - INTERVAL '2 days'),

    (1005, 'Checked out "The Hunger Games".',
        CURRENT_TIMESTAMP - INTERVAL '10 days'),

    (1006, 'Checked out "Frankenstein".',
        CURRENT_TIMESTAMP - INTERVAL '4 days'),

    (1007, 'Checked out "Ready Player One".',
        CURRENT_TIMESTAMP - INTERVAL '1 day'),

    (1008, 'Reserved "1984".',
        CURRENT_TIMESTAMP - INTERVAL '2 days'),

    (1006, 'Reserved "1984".',
        CURRENT_TIMESTAMP - INTERVAL '1 day'),

    (1003, 'Reserved "The Hobbit".',
        CURRENT_TIMESTAMP - INTERVAL '4 days');

INSERT INTO admin_access
    (id, access_code, expires_at)
VALUES
    (
        1,
        583214,
        CURRENT_TIMESTAMP + INTERVAL '15 minutes'
    );