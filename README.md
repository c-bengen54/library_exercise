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

````

### `application_db/README.md`

# Library Management System — Flask Application

A work-in-progress web-based Library Management System built with Python, Flask, and PostgreSQL.

This repository contains the next stage of the Library Management System, transitioning the project from a terminal-based application into a browser-accessible web application.

The project builds upon the database and application architecture developed in the terminal version while introducing Flask, HTML/CSS, session-based authentication, and a web interface.

## Current Status

**Work in progress.**

The core Flask application, database integration, authentication, and primary library functionality are currently implemented. Several components remain under development before the application can be considered production-ready.

### Remaining Development

* Administrator functionality
* Advanced search systems
* Due dates
* Overdue tracking
* Expanded logging
* Custom error handling
* Containerization
* Production deployment/rollout

## Implemented Features

* Flask web application
* User registration
* User login
* Session-based authentication
* Password hashing with `bcrypt`
* PostgreSQL database integration
* Book management
* Book searching
* Book checkout
* Book returns
* Book reservations
* Viewing borrowed books
* Viewing reservations
* Database-backed persistent storage
* ISBN-10 and ISBN-13 validation
* Database functions and constraints
* HTML/CSS web interface

## Technologies

* **Python** — application logic
* **Flask** — web application framework
* **PostgreSQL** — persistent database
* **psycopg** — Python/PostgreSQL connection
* **bcrypt** — password hashing
* **PL/pgSQL** — database-side functions and validation
* **HTML/CSS** — web interface
* **Jinja2** — Flask templating
* **Git/GitHub** — version control

## Application Architecture

The application is separated into several layers:

```text
Browser
   │
   ▼
Flask Routes / Blueprints
   │
   ▼
Application Logic
   │
   ▼
Database Functions
   │
   ▼
PostgreSQL
````

Flask handles HTTP requests and renders the web interface, while the database layer handles communication with PostgreSQL.

This separation allows the web interface to interact with the same underlying library data without placing database operations directly inside the HTML templates.

## Project Structure

```text
library_exercise/
│
├── database/
│   ├── db.py
│   ├── db_book.py
│   └── db_member.py
│
├── templates/
│   └── ...
│
├── static/
│   └── ...
│
├── auth.py
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

> The structure is subject to change as development continues.

## Database

The Flask application uses PostgreSQL for persistent storage.

The database currently contains tables for:

* Users
* Books
* Borrowed books
* Reservations
* Logs
* Administrator access

### Users

Stores registered users and their account information, including authentication data and user type.

Passwords are stored as hashes rather than plaintext passwords.

### Books

Stores library book information and tracks whether each book is currently checked out.

ISBN values are validated using a PostgreSQL function.

### Borrowed Books

Associates members with books they currently have borrowed and records the borrowing time.

### Reservations

Stores reservations made by members for books that are unavailable.

### Logs

Provides a database-backed system for recording application events. Additional logging functionality remains under development.

### Administrator Access

The database includes support for administrator access codes.

The intended system uses periodically changing access codes rather than relying solely on a permanent administrator password. Further administrator functionality remains to be implemented.

## Authentication

Users can register and log into the application through the Flask web interface.

After successful authentication, Flask sessions are used to associate requests with the currently logged-in user.

This allows the application to display user-specific information such as:

* Borrowed books
* Reservations
* Account information

Passwords are protected using `bcrypt` hashing.

## ISBN Validation

A PostgreSQL PL/pgSQL function validates ISBN-10 and ISBN-13 values.

The function performs format and checksum validation and is used by a database constraint to prevent invalid ISBN values from being stored.

## Configuration

Database credentials and other sensitive configuration values should not be committed to Git.

The application should be configured through environment variables or an equivalent secure configuration system.

A `.env` file may be used for local development when appropriate, provided that it is excluded from version control through `.gitignore`.

## Installation

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required database connection settings.

## Running the Application

The Flask application can currently be run in a development environment using Flask's development server.

For example:

```bash
flask run
```

The exact startup command may change as the application architecture develops.

## Development Roadmap

The remaining work is divided into several major areas:

### Administrator Functionality

Complete the administrator interface and associated permissions for managing the library.

### Search Systems

Expand the existing search functionality to support more advanced searching and filtering.

### Due Dates and Overdue Tracking

Add due dates to borrowed books and implement logic for identifying overdue items.

### Logging

Expand the existing database logging system to provide more comprehensive application activity tracking.

### Custom Error Handling

Implement custom Flask error pages and centralized error handling for expected application errors.

### Containerization

Package the application and its dependencies into containers to make deployment more consistent.

### Production Rollout

Prepare the application for production deployment, including production server configuration, environment management, and deployment infrastructure.

## Relationship to `web_db`

`web_db` contains the terminal-based version of the Library Management System.

That project transitioned the application from using a locally managed PostgreSQL database to a remotely hosted PostgreSQL database.

`application_db` represents the next stage of development: transforming the system into a Flask web application that can be accessed through a browser.

The two repositories therefore represent different stages of the same overall project:

```text
Terminal Application
       │
       │ Remote PostgreSQL integration
       ▼
    web_db
       │
       │ Flask/web migration
       ▼
 application_db
       │
       │ Production development
       ▼
 Future Production LMS
```

## Future Goals

The ultimate goal is to turn the current Flask application into a fully deployable Library Management System with:

* Complete member functionality
* Complete administrator functionality
* Advanced searching
* Borrowing and reservation management
* Due dates and overdue tracking
* Comprehensive logging
* Robust error handling
* Secure configuration
* Containerized deployment
* Production hosting
* Automated testing

## License

This project is primarily intended as an educational/student project.

```

**`web_db` is the working terminal implementation, while `application_db` is the unfinished Flask successor.**
```
