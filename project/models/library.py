from models.user import Admin, Member, ADMIN_CODE
from datetime import datetime
import random

class Book:
    def __init__(self, title:str, author:str, publication:int, genre:str, checked_out: bool = False):
        self.title = title
        self.author = author
        self.publication = publication
        self.genre = genre
        self.checked_out = checked_out
        self.holder = None

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication})"
    
    def display_info(self):
        print(f"{self.title} by {self.author} ({self.publication}) [{self.genre}]")

        if self.holder is not None:
            print(f"Currently held by: {self.holder.name} ")
        else:
            print("Available")

        if self.checked_out:
            print("Status: Checked out\n")
        elif not self.checked_out:
            print("Status: In circulation\n")
        else:
            print("Status: Unknown\n")

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.admins = []
        self.reservation_queue = {}

    def add_book(self, book:Book):
        
        if isinstance(book, list):
            self.books.extend(book)
        
        else:
            self.books.append(book)

    def remove_book(self, book:Book):
        self.books.remove(book)

    def register_member(self, member_name:str):
        
        if any(member.name == member_name for member in self.members):
            print("Name has been taken")
       
        else:
            member_id = random.randint(111111, 999999)
            new_member = Member(member_name, member_id)
            self.members.append(new_member)
            new_member.log_event(f"Library registered new member: {member_name} | {datetime.now()}", True)

    def register_admin(self, admin_name:str, admin_code:int):
        
        if admin_code == ADMIN_CODE:
            if any(admin.name == admin_name for admin in self.admins):
                print("Name already taken")
        
            else:
                admin_id = random.randint(111111, 999999)
                unique_admin_code = random.randint(111111, 999999)
                new_admin = Admin(admin_name, admin_id, unique_admin_code)
                self.admins.append(new_admin)
                new_admin.log_event(f"Library registered new admin: {admin_name} | {datetime.now()}", True)

        else:
            print("Incorrect admin code")

    def search_by_title(self, title:str):        
        for book in self.books:
            if title == book.title:
                book.display_info()
            
    def search_by_author(self, author:str):        
        for book in self.books:
            if author == book.author:
                book.display_info()
        
    def list_available_books(self):
        for book in self.books:
            book.display_info()

    def is_checked_out(self, book:Book):
        return book.checked_out
        
    def check_out(self, member:Member, book:Book):
        
        if member not in self.members:
            raise Exception("Member not registered, please register with the library before you check out a title")
        
        if book not in self.books:
            raise Exception("Book not in catalogue, check again at a later date")
        
        if book.checked_out:
            raise Exception("The book has been checked out")
        
        if book in member.reservations:
            member.reservations.remove(book)

        book.checked_out = True
        book.holder = member
        member.borrowed_books.append(book)
                    
        member.log_event(f"Member: {member.name} checked out title: {book.title} | {datetime.now()}", False)
        member.log_event(f"Member: {member.name} checked out title: {book.title} | {datetime.now()}", True)
                
    def reserve_book(self, member:Member, book:Book):
        if member not in self.members:
            raise Exception("Member not registered")

        if book not in self.books:
            raise Exception("Book not found")

        if not book.checked_out:
            raise Exception("Book is available to check out.")

        if member == book.holder:
            raise Exception("You already have this book checked out.")

        if book not in self.reservation_queue:
            self.reservation_queue[book] = []

        if member in self.reservation_queue[book]:
            raise Exception("You already have this reservation.")

        self.reservation_queue[book].append(member)
        member.reservations.append(book)

        member.log_event(f"Member: {member.name} reserved title: {book.title} | {datetime.now() }", False)
        member.log_event(f"Member: {member.name} reserved title: {book.title} | {datetime.now() }", True)
    
    def return_book(self, member:Member, book:Book):
        if member not in self.members:
            raise Exception("User is not a member of the library")

        if book.holder != member:
            raise Exception("That member doesn't currently hold this book.")

        if book in self.reservation_queue:
            next_member = self.reservation_queue[book].pop(0)
            self.check_out(next_member, book)

        book.checked_out = False
        book.holder = None
        member.borrowed_books.remove(book)
        member.log_event(f"Member: {member.name} returned title: {book.title} | {datetime.now()}", False)
        member.log_event(f"Member: {member.name} returned title: {book.title} | {datetime.now()}", True)

    def select_user(self, member:str, mode:str) -> Member:
        if mode == "member":
            for x in self.members:
                if x.name == member:
                    return x
                
            raise Exception("User not found")
                
        if mode == "admin":
            for x in self.admins:
                if x.name == member:
                    return x
                
            raise Exception("User not found")

    def select_book(self, title:str) -> Book:
        for book in self.books:
            if book.title == title:
                return book
        raise ValueError(f"Book not found with title: {title}, or has not yet been registered")