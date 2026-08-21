from database.db_book import *
from database.db_member import *
from datetime import datetime, timezone
import random, secrets

access = initialize_admin_code()

class Library:

    def add_book(self, title:str, author:str, pub:int, genre:str, isbn:str):
        """
        Adds a new book to the library database.

        Parameters:
            title (str):
                Title of the book.
            author (str):
                Author of the book.
            pub (str):
                Publication year of the book.
            genre (str):
                Genre or category of the book.
            isbn (str):
                ISBN-10 or ISBN-13 identifier for the book.

        Returns:
            None
        """
        db_add_book(title, author, pub, genre, isbn)

    def remove_book(self, book_id:int):
        """
        Removes a book from the library database.

        Parameters:
            book_id (int):
                Unique database ID of the book to remove.

        Returns:
            None
        """
        db_delete_book(book_id)

    def register_user(self, username:str, m_first_name:str, m_last_name:str, m_email:str, password_hash:bytes, user_type:str, admin_code:int = None):
        """
        Registers a new member or administrator.

        A valid administrator access code is required when registering
        an administrator account.

        Parameters:
            username (str):
                Username for the new account.
            m_first_name (str):
                First name of the user.
            m_last_name (str):
                Last name of the user.
            m_email (str):
                Email address of the user.
            password (bytes):
                Password hash for the account.
            user_type (str):
                Type of account being created, such as "member" or
                "admin".
            admin_code (int, optional):
                Current administrator access code. Required when
                user_type is "admin". Defaults to None.

        Returns:
            int:
                If registration is successful, returns the member ID.

            None:
                If an invalid administrator code is provided.
        """
        if user_type.lower().strip() == "admin" and admin_code != access[0]:
            return None

        while True:
            member_id = random.randint(100000, 999999)
            if db_find("users", "user_id", member_id) is None:
                break
        
        db_register_user(member_id, username, m_first_name, m_last_name, m_email, password_hash, user_type)

        db_log_event(member_id, f"Library registered new user: {username} | User Type: {user_type}", datetime.now(timezone.utc))

        return member_id

    def search_by_title(self, title:str):  
        """
        Searches the library for a book with the specified title.

        Parameters:
            title (str):
                Exact title of the book to search for.

        Returns:
            tuple | None:
                The matching book record, or None if no book is found.
        """      
        return db_get_book_by("title", title)
            
    def search_by_author(self, author:str): 
        """
        Searches the library for a book by author.

        Parameters:
            author (str):
                Author name to search for.

        Returns:
            tuple | None:
                The first matching book record, or None if no book is found.
        """       
        return db_get_book_by("author", author)
        
    def list_available_books(self):
        """
        Retrieves all books that are currently available for checkout.

        Parameters:
            None

        Returns:
            list:
                List of books that are not currently checked out.
        """
        return db_get_all_books()

    def is_checked_out(self, book_id:int):
        """
        Checks whether a specific book is currently checked out.

        Parameters:
            book_id (int):
                Unique ID of the book to check.

        Returns:
            tuple | None:
                A tuple containing the book's checkout status, or None
                if the book does not exist.
        """
        return db_is_checked_out(book_id)
        
    def check_out(self, member_id:int, book_id:int):
        """
        Checks a book out to a member.

        Raises an exception if the requested book is already checked out.
        A checkout event is also recorded in the system log.

        Parameters:
            member_id (int):
                Unique ID of the member borrowing the book.
            book_id (int):
                Unique ID of the book being borrowed.

        Returns:
            None

        Raises:
            Exception:
                If the book is already checked out.
        """
        flag = db_is_checked_out(book_id)
        if flag[0]:
            raise Exception("Book is already checked out")
        
        db_check_out(member_id, book_id)
        db_log_event(member_id,f"{member_id} checked out title: {book_id}", datetime.now())
                
    def reserve_book(self, member_id:int, book_id:int):
        """
        Adds a member to the reservation queue for a book.

        A book can only be reserved when it is currently checked out.
        The reservation is recorded in the database and in the system
        log.

        Parameters:
            member_id (int):
                Unique ID of the member making the reservation.
            book_id (int):
                Unique ID of the book being reserved.

        Returns:
            None

        Raises:
            Exception:
                If the book is currently available for checkout.
        """
        flag = db_is_checked_out(book_id)
        if not flag[0]:
            raise Exception("Book is available for check out")
        
        db_reserve_book(book_id, member_id)

        db_log_event(member_id, f"Member: {member_id} reserved title: {book_id}", datetime.now())
    
    def return_book(self, member_id, book_id: int):
        """
        Returns a book to the library and processes the next reservation.

        If members are waiting for the returned book, the first member
        in the reservation queue automatically receives the book.

        Parameters:
            member_id (int):
                Unique ID of the member returning the book.
            book_id (int):
                Unique ID of the book being returned.

        Returns:
            None
        """
        db_return_book(book_id)
        
        next_holder = db_get_reservation(book_id)
        if next_holder:
            db_check_out(next_holder[0][2], book_id)
            db_cancel_reservation(book_id, next_holder[0][2])

        db_log_event(member_id, f"Member: {member_id} returned title: {book_id}", datetime.now(timezone.utc))

    def select(self, data:str, query:str, param):
        """
        Searches a specified database table for a matching record.

        Parameters:
            data (str):
                Name of the database table to search.
            query (str):
                Name of the column to search.
            param:
                Value to search for. The type should match the selected
                column.

        Returns:
            tuple | None:
                The first matching database record, or None if no record
                is found.
        """
        return db_find(data, query, param)

    def update_user(self, change_value:str, new_value, member_id:int):
        """
        Updates a specific field belonging to an existing user.

        Parameters:
            change_value (str):
                Name of the users table column that should be changed.
            new_value:
                New value for the specified column. The type must match
                the database column.
            member_id (int):
                Unique ID of the user being updated.

        Returns:
            None

        Raises:
            Exception:
                If a user with the specified ID does not exist.
        """
        if db_find("users", "user_id", member_id):
            db_update_member(change_value, new_value, member_id)
        else:
            raise Exception("User not found")

    def view_logs(self):
        """
        Retrieves all recorded library system events.

        Parameters:
            None

        Returns:
            list:
                List of all log records stored in the database.
        """
        return db_view_logs()