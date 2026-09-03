# Library Management System — Terminal Application

A Python-based Library Management System operated through a terminal interface and backed by a remotely hosted PostgreSQL database.

This version of the project represents the completed terminal-based implementation of the Library Management System. The application was originally designed around a locally managed PostgreSQL database and was later adapted to use a remotely hosted database, allowing the application and database to operate independently.

The project demonstrates object-oriented programming, SQL, PostgreSQL integration, database-side validation, authentication, borrowing and reservation management, and persistent data storage.

## Features

* Add and remove books from the library
* Search for books by title or author
* View available books
* Check books out to members
* Return borrowed books
* Reserve books that are currently unavailable
* Maintain reservation information
* Register library members
* Register administrators
* Track borrowing activity
* Store library data in a remotely hosted PostgreSQL database
* Validate ISBN-10 and ISBN-13 numbers
* Use PostgreSQL functions and constraints for data validation
* Maintain persistent data independently of the local application
* Connect to the database through Python using `psycopg`

## Technologies

* **Python** — application logic and object-oriented design
* **PostgreSQL** — persistent data storage
* **psycopg** — Python/PostgreSQL database connection
* **PL/pgSQL** — database-side functions and validation
* **Git/GitHub** — version control

## Project Structure

```text
library_exercise/
│
├── database/
│   ├── db.py
│   ├── db_book.py
│   └── db_member.py
│
├── database_setup/
│   ├── schema.sql
│   └── sample_data.sql
│
├── models/
│   └── ...
│
├── main.py
├── library.py
├── book.py
├── user.py
├── member.py
├── admin.py
│
├── sql/
│   └── ...
│
├── .gitignore
├── requirements.txt
└── README.md
```

> The exact filenames and directories may vary depending on the current version of the project.

## Database

The application uses PostgreSQL as its persistent data layer.

The database contains tables for users, books, borrowing records, reservations, application logs, and administrator access.

### Users

Stores registered members and administrators, including:

* User ID
* Username
* Name
* Email
* Password hash
* User type

### Books

Stores library books, including:

* Title
* Author
* Publication year
* Genre
* ISBN
* Checkout status
* Current holder

ISBN values are validated using a PostgreSQL function before being accepted.

### Borrowing

Borrowing records associate members with books and record when books were borrowed.

### Reservations

Reservations associate members with books that are currently unavailable.

### Logs

Application activity can be recorded in the database for later review.

### Administrator Access

The database contains the information required to support administrator access and periodically changing administrator access codes.

## ISBN Validation

The database contains a PL/pgSQL function used to validate ISBN-10 and ISBN-13 values.

The validation process:

1. Removes formatting characters such as hyphens.
2. Converts the value to uppercase.
3. Determines whether it is an ISBN-10 or ISBN-13.
4. Checks that the format is valid.
5. Calculates the appropriate checksum.
6. Returns whether the ISBN is valid.

The function is also used by a database constraint so that invalid ISBN values cannot be inserted into the books table.

## Remote Database

Unlike the earlier local-database version of the project, this version connects to a remotely hosted PostgreSQL database.

This allows:

* The database to remain available independently of the local machine.
* Multiple application instances to access the same database.
* Database data to persist independently of the application files.
* The project to serve as a foundation for the later web application.

Database credentials should **not** be committed to the repository. They should instead be provided through environment variables or another secure configuration method.

## Installation

Clone the repository and create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Configure the PostgreSQL connection using the appropriate environment variables.

## Running the Program

After configuring the database connection, run:

```bash
python main.py
```

The application can then be operated through the terminal interface.

## Version Control

Git is used to track changes to the project.

Sensitive configuration files, virtual environments, Python cache files, and other generated files should be excluded through `.gitignore`.

## Relationship to `application_db`

`web_db` is the terminal-based version of the Library Management System.

`application_db` is the subsequent web-application version being developed with Flask. The Flask application is intended to provide a browser-based interface while retaining the PostgreSQL-backed application architecture developed in this project.

## Future Improvements

* Complete migration to the Flask web application
* Administrator functionality in the web interface
* Advanced search and filtering
* Due dates and overdue tracking
* Improved reservation management
* Expanded logging and reporting
* Custom application error handling
* Automated database setup
* Unit and integration testing
* Containerization
* Production deployment

## License

This project is primarily intended as an educational/student project.
```
`web_db` is the working terminal implementation, while `application_db` is the unfinished Flask successor.
```
