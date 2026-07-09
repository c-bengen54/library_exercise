from models.user import Admin, Member, ADMIN_CODE, User
from datetime import datetime
import json, os, random

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

    def register_member(self, member_name:str) -> Member:
        
        if any(member.name == member_name for member in self.members):
            print("Name has been taken")
       
        else:
            member_id = random.randint(111111, 999999)
            new_member = Member(member_name, member_id)
            self.members.append(new_member)
            new_member.log_event(f"Library registered new member: {member_name} | {datetime.now()}", True)
            return new_member

    def register_admin(self, admin_name, admin_code):

        if admin_code != ADMIN_CODE:
            print("Wrong admin code")
            return None

        if any(admin.name == admin_name for admin in self.admins):
            print("Duplicate admin name")
            return None

        admin_id = random.randint(111111, 999999)
        unique_admin_code = random.randint(111111, 999999)

        new_admin = Admin(admin_name, admin_id, unique_admin_code)


        self.admins.append(new_admin)
        new_admin.log_event(f"Library registered new admin: {admin_name} | {datetime.now()}", True)

        return new_admin

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
    
    def save(self, filepath:str = "library.json"):
        data = {
            "books": [],
            "members": [],
            "admins": [],
            "reservation_queue": {},
            "log": User.global_log

        }

        for book in self.books:
            data["books"].append({
                "title": book.title,
                "author": book.author,
                "publication": book.publication,
                "genre": book.genre,
                "checked_out": book.checked_out,
                "holder": book.holder.name if book.holder else None
            })

        for member in self.members:
            data["members"].append({
                "name": member.name,
                "user_id": member.user_id,
                "borrowed_books":[book.title for book in member.borrowed_books],
                "reservations":[reservation.title for reservation in member.reservations],
                "log": member.log,
            })

        for admin in self.admins:
            data["admins"].append({
                "name": admin.name,
                "user_id": admin.user_id,
                "admin_id": admin.admin_id,
                "log": admin.log,
            })

        for book, people in self.reservation_queue.items():
            data["reservation_queue"][book.title] = [
                member.name for member in people
            ]

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        
    @classmethod
    def load(cls, filepath):
        library = cls()

        if not os.path.exists(filepath):
            raise Exception("File does not exist")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                save = json.load(f)
        except Exception as e:
            raise FileNotFoundError(f"Error happened while loading save {e}")
        
        books = {}

        for info in save["books"]:
            book = Book(info["title"], 
                        info["author"], 
                        info["publication"], 
                        info["genre"], 
                        info["checked_out"])
            
            library.books.append(book)
            books[book.title] = book

        members = {}

        for info in save["members"]:
            member = Member(info["name"], info["user_id"])

            member.log = info["log"]

            library.members.append(member)

            members[member.name] = member

        for info in save["members"]:
            member = members[info["name"]]

            for title in info.get("borrowed_books", []):
                member.borrowed_books.append(books[title])

            for title in info.get("reservations", []):
                member.reservations.append(books[title])

        for info in save["books"]:
            if info["holder"]:
                books[info["title"]].holder = members[
                    info["holder"]
                ]

        for info in save["admins"]:
            admin = Admin(
                info["name"],
                info["user_id"],
                info["admin_id"]
            )

            admin.log = info["log"]

            library.admins.append(admin)

        for title, names in save["reservation_queue"].items():
            library.reservation_queue[books[title]] = [
                members[name]
                for name in names
            ]

        User.global_log = save["log"]

        return library