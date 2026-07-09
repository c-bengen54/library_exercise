from datetime import datetime
from enum import Enum

ADMIN_CODE = 540146

class Status(Enum):
    BORROW = 1
    RESERVATION = 2

class User:
    global_log = []

    def __init__(self, name:str, user_id:int):
        self.name = name
        self.user_id = user_id
        self.log = []

    def log_event(self, message:str, global_flag:bool):
        if global_flag and message is not None:
            User.global_log.append("[Global] " + message + "\n")
        elif not global_flag and message is not None:
            self.log.append(message + "\n")
        else:
            raise Exception("Log message is empty")

class Member(User):
    def __init__(self, name:str, member_id:int):
        super().__init__(name, member_id)
        self.reservations = []
        self.borrowed_books = []

    def __str__(self):
        return f"User: {self.name} | ID: {self.user_id}"

    def list_books(self):
            for book in self.borrowed_books:
                print("- " + book.title)
    
    def list_reservations(self):
        for reservation in self.reservations:
            print("- " + reservation.title)

class Admin(User):
    def __init__(self, name:str, user_id:int, admin_id:int):
        super().__init__(name, user_id)
        self.admin_id = admin_id

    def __str__(self):
        return f"User: {self.name} | ID: {self.user_id} | ADMIN_ID: {self.admin_id}"

    def update_id(self, member:Member, new_id:int):
        old_id = member.user_id
        member.user_id = new_id
        self.log_event(f"\nAdmin: {self.name} updated a users ID: {old_id} to {new_id} | {datetime.now()}", False)
        self.log_event(f"\n[Global] Admin: {self.name} updated a users ID | {datetime.now()}", True)

    def update_name(self, member:Member, new_name:str):
        old_name = member.name
        member.name = new_name
        self.log_event(f"Admin: {self.name} changed Users: {old_name} name to {new_name} | {datetime.now()}", False)
        self.log_event(f"Admin: {self.name} updated a users name | {datetime.now()}", True)

    def view_member_log(self, member:Member):
        for item in member.log:
            print(item)

    def view_global_log(self):
        for item in User.global_log:
            print(item)

    def review_member(self, member:Member, review_option:Status):
        print(f"Currently reviewing User: {member.name}\n")

        if review_option == Status.BORROW:
            for book in member.borrowed_books:
                print("- " + book.title + "\n")
        elif review_option == Status.RESERVATION:
            for book in member.reservations:
                print("- " + book.title + "\n")