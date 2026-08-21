# Library Management System

A Python-based Library Management System backed by a PostgreSQL database. The project provides functionality for managing books, members, administrators, borrowing, returning, and reservations while demonstrating object-oriented programming, SQL, database integration, and data validation.

## Features

* Add and remove books from the library
* Search for books by title or author
* View available books
* Check books out to members
* Return borrowed books
* Reserve books that are currently unavailable
* Maintain a reservation queue
* Register library members
* Register administrators
* Track borrowing activity
* Store library data in PostgreSQL
* Validate ISBN-10 and ISBN-13 numbers
* Use PostgreSQL functions and constraints for data validation

## Technologies

* **Python** — application logic and object-oriented design
* **PostgreSQL** — persistent data storage
* **psycopg** — Python/PostgreSQL database connection
* **PL/pgSQL** — database-side ISBN validation
* **Git/GitHub** — version control

## Project Structure

```text
library_exercise/
│
├── main.py
├── db.py
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

> The exact filenames may vary depending on the current version of the project.

## Database

The application uses PostgreSQL to persist library information.

The database contains tables for information such as:

* Books
* Members/users
* Borrowed books
* Reservations

The database is responsible for storing information that needs to persist when the program is closed and restarted.

### Books

The books table stores information such as:

* Title
* Author
* Publication year
* Genre
* ISBN
* Checkout status

### Borrowing

When a member checks out a book, the database records the borrowing relationship. When the book is returned, its availability is updated.

### Reservations

If a book is already checked out, members can place a reservation. Reservations can be maintained in order so that the next eligible member can receive the book when it becomes available.

## ISBN Validation

The project includes a PostgreSQL function called `fn_isbn` that validates ISBN numbers.

The function:

1. Removes hyphens from the ISBN.
2. Converts the input to uppercase.
3. Determines whether it is an ISBN-10 or ISBN-13.
4. Validates the appropriate checksum.
5. Returns `TRUE` for a valid ISBN and `FALSE` otherwise.

This validation is performed at the database level rather than relying entirely on the Python application.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd library_exercise
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Make sure PostgreSQL is installed and running.

Create the database:

```sql
CREATE DATABASE library_db;
```

Then connect to the database:

```bash
psql -d library_db
```

Run the project's SQL setup scripts to create the required tables, functions, constraints, and other database objects.

## Configuration

Database connection information should be configured locally rather than committed to the repository.

For example:

```text
Database: library_db
Host: localhost
Port: 5432
```

Any passwords or other sensitive credentials should be kept out of Git and stored using an appropriate local configuration or environment-variable system.

## Running the Program

After PostgreSQL is running and the database has been configured, activate the virtual environment and run the application:

```bash
source venv/bin/activate
python main.py
```

The exact entry point may vary depending on the current project structure.

## Version Control

The project uses Git for version control.

The repository's `.gitignore` prevents generated or local-only files from being committed, including Python cache files and the virtual environment:

```gitignore
__pycache__/
*.pyc
venv/
.venv/
```

This keeps the repository focused on the source code and project files needed to recreate the application.

## Project Goals

This project was created to practice combining several areas of computer science into a single application, including:

* Object-oriented programming
* Relational databases
* SQL
* PostgreSQL
* Database design
* Python database connectivity
* Data validation
* CRUD operations
* Version control with Git

The project also demonstrates how an application can move from local file-based storage to a proper relational database system.

## Future Improvements

Potential future additions include:

* A graphical user interface
* Improved authentication and administrator access
* More advanced search and filtering
* Improved reservation management
* Due dates and overdue tracking
* Fines for overdue books
* Expanded reporting and statistics
* Automated database setup
* Unit and integration testing

## License

This project is intended primarily as an educational/student project.
