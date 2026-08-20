from database.db_book import *
from database.db_member import *
from datetime import datetime
import random, secrets

access = initialize_admin_code()

class Library:

    def add_book(self, title:str, author:str, pub:str, genre:str, isbn:str):
        db_add_book(title, author, pub, genre, isbn)

    def remove_book(self, book_id:int):
        db_delete_book(book_id)

    def register_member(self, username:str, m_first_name:str, m_last_name:str, m_email:str, password:bytes):

        while True:

            member_id = random.randint(100000, 999999)
            if db_find("members", "user_id", member_id) is None:
                break
        
        db_register_member(member_id, username, m_first_name, m_last_name, m_email, password)

        db_log_event(member_id, f"Library registered new member: {username}", datetime.now())

    def register_admin(self, admin_name:str, admin_code:int):

        if admin_code != access[0]:
            print("Wrong admin code")
            return None

        while True:
        
            admin_id = random.randint(100000, 999999)
            if db_find("admins", "user_id", admin_id) is None:
                break

        db_register_admin(admin_name, admin_id)

        db_log_event(admin_id, f"Library registered new admin: {admin_name}", datetime.now() )

    def search_by_title(self, title:str):        
        return db_get_book_by("title", title)
            
    def search_by_author(self, author:str):        
        return db_get_book_by("author", author)
        
    def list_available_books(self):
        return db_get_all_books()

    def is_checked_out(self, book_id:int):
        return db_is_checked_out(book_id)
        
    def check_out(self, member_id:int, book_id:int):
        flag = db_is_checked_out(book_id)
        if flag[0]:
            raise Exception("Book is already checked out")
        
        db_check_out(member_id, book_id)
        db_log_event(member_id,f"{member_id} checked out title: {book_id}", datetime.now())
                
    def reserve_book(self, member_id:int, book_id:int):

        flag = db_is_checked_out(book_id)
        if not flag[0]:
            raise Exception("Book is available for check out")
        
        db_reserve_book(book_id, member_id)

        db_log_event(member_id, f"Member: {member_id} reserved title: {book_id}", datetime.now())
    
    def return_book(self, member_id, book_id: int):

        db_return_book(book_id)
        
        next_holder = db_get_reservation(book_id)
        if next_holder:
            db_check_out(next_holder[0][2], book_id)
            db_cancel_reservation(book_id, next_holder[0][2])

        db_log_event(member_id, f"Member: {member_id} returned title: {book_id}", datetime.now())

    def select(data:str, query:str, param):
        return db_find(data, query, param)

    def update_user(change_value:str, new_value, member_id:int):
        if db_find("members", "user_id", member_id):
            db_update_member(change_value, new_value, member_id)
        else:
            raise Exception("User not found")

    def view_logs():
        return db_view_logs()