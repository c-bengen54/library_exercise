import time
import bcrypt
from models.library import Library, Book

library = Library()
salt = bcrypt.gensalt()


def get_input(question:str, conversion:bool = False) -> str | int:
    if conversion:
        while True:
            try:
                user_input = input(question)
                user_input = int(user_input)
                break
            except (KeyboardInterrupt, EOFError, ValueError):
                print(color_text("\nIncorrect input type, please try again\n", "red"))
                continue
        return user_input
    
    if not conversion:
        while True:
            try:
                user_input = input(question)
                break
            except (KeyboardInterrupt, EOFError, ValueError):
                print(color_text("\nIncorrect input type, please try again\n", "red"))
                continue
        return user_input

def color_text(text:str, color:str = "end") -> str:
    """Return a colorized string of text"""
    colors = {
        "bold": "\033[1m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "italic": "\033[3m",
        "end": "\033[0m"
        }
    return f"{colors.get(color, '')}{text}{colors['end']}"

def main_menu():
    time.sleep(0.5)
    while True:
        print("\n===== Main Menu =====")
        print("1. Login Member")
        print("2. Login Admin")
        print("3. Register Member")
        print("4. Register Admin")
        print("5. Exit\n")
        
        user_input = get_input("> ", True)

        if user_input == 1:
            member_login()
            
        elif user_input == 2:
            admin_login()

        elif user_input == 3:
            member_name = get_input("\nInput requested name: ")
            new_member = library.register_member(member_name)
            print("\nAccount registered", color_text(f"\n{new_member}", "green"))
            library.save()

        elif user_input == 4:
            admin_name = get_input("\nInput requested name: ")
            admin_code = get_input("\nInput admin registration code: ", True)
            new_admin = library.register_admin(admin_name, admin_code)
            print("\nAdmin registered", color_text(f"\n{new_admin}", "green"))
            library.save()

        elif user_input ==5:
            print(color_text("\nExiting program...", "yellow"))
            time.sleep(2)
            print(color_text("\n- Have a wonderful day!!\n", "cyan"))
            library.save()
            break

        else:
            print(color_text("\nInputted option either not in menu, or incorrect input type. \nPlease try again.\n", "red"))
            time.sleep(2)

def member_login():
    username = get_input("\nUsername: ")
    user_id = get_input("\nID: ", True)

    for member in library.members:
        if member.name == username and member.user_id == user_id:
            print(color_text("\nEntering member menu.....", "yellow"))
            time.sleep(2)
            member_menu(member.name)
            return

    print(color_text("\nInvalid username or ID.\n", "red"))

def admin_login():
    username = get_input("\nUsername: ")
    user_id = get_input("\nUser ID: ", True)
    admin_id = get_input("\nAdmin ID: ", True)
    for admin in library.admins:
        if admin.name == username and admin.user_id == user_id and admin.admin_id == admin_id:
            print(color_text("\nEntering admin menu.....", "yellow"))
            time.sleep(2)
            admin_menu(admin.name)
            return
    
    print(color_text("\nInvalid username, user ID or admin ID", "red"))

def member_menu(member_name):
    user = library.select_user(member_name, "member")

    while True:
        print("\n===== Member Menu =====")
        print("1. Checkout Book")
        print("2. Reserve Books")
        print("3. View Catalogue")
        print("4. Search by Author")
        print("5. Search by Title")
        print("6. List Reserved Titles")
        print("7. List Borrowed Titles")
        print("8. Exit\n")

        user_input  = get_input("> ", True)

        if user_input == 1:
            title = get_input("Input title you wish to check out > ")
            book = library.select_book(title)
            library.check_out(user, book)
            print(color_text("Title sucessfully checked out", "green"))
            library.save()
            

        elif user_input == 2:
            title = get_input("Input title you wish to reserve > ")
            book = library.select_book(title)
            library.reserve_book(user, book)
            print(color_text("Title sucessfully reserved", "green"))
            library.save()

        elif user_input == 3:
            library.list_available_books()
            time.sleep(2)

        elif user_input == 4:
            author = get_input("Input name of author > ")
            library.search_by_author(author)

        elif user_input == 5:
            title = get_input("Input title of book > ")
            library.search_by_title(title)

        elif user_input == 6:
            user.list_reservations()

        elif user_input == 7:
            user.list_books()

        elif user_input == 8:
            print(color_text("Exiting member menu.....", "yellow"))
            time.sleep(2)
            break

        else:
            continue

def admin_menu(admin_name):
    admin = library.select_user(admin_name, "admin")
    
    while True:
        print("\n===== Admin Menu =====")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Update User Name")
        print("4. Update User ID")
        print("5. View Member Log")
        print("6. View Global Log")
        print("7. Exit\n")

        user_input  = get_input("> ", True)

        if user_input == 1:
            title = get_input("Input title > ")
            author = get_input("Input books author > ")
            publication = get_input("Input Publication Year > ", True)
            genre = get_input("Input book genre > ")
            book = Book(title, author, publication, genre)
            library.add_book(book)
            print(color_text("\nBook added to catalogue successfully", "green"))
            library.save()

        elif user_input == 2:
            title = get_input("Input title to be removed > ")
            book_for_removal = library.select_book(title)
            library.remove_book(book_for_removal)
            print(color_text("\nBook removed from catalogue successfully", "green"))
            library.save()

        elif user_input == 3:
            member_name = get_input("Input members username > ")
            requested_name = get_input("Input requested name > ")
            member = library.select_user(member_name, "member")
            admin.update_name(member, requested_name)
            print(color_text("\nName updated successfully", "green"))
            library.save()

        elif user_input == 4:
            member_name = get_input("Input members username > ")
            requested_id = get_input("Input new ID > ", True)
            member = library.select_user(member_name, "member")
            admin.update_id(member, requested_id)
            print(color_text("\nUser's ID updated successfully", "green"))
            library.save()

        elif user_input == 5:
            member_name = get_input("Input username to view log > ")
            member = library.select_user(member_name, "member")
            admin.view_member_log(member)
            time.sleep(2)

        elif user_input == 6:
            admin.view_global_log()
            time.sleep(2)

        elif user_input == 7:
            print(color_text("Exiting admin menu.....", "yellow"))
            time.sleep(2)
            break

        else:
            continue 

member_names = [
    "Chris",
    "James",
    "Olivia",
    "Emma",
    "Liam",
    "Noah",
    "Sophia",
    "Charlotte",
    "Benjamin",
    "Lucas",
    "Amelia",
    "Mason",
    "Evelyn",
    "Henry",
    "Abigail"
]

admin_names = [
    "Sarah",
    "Michael",
    "Daniel",
    "Victoria",
    "Anthony",
    "Grace",
    "Thomas",
    "Natalie"
]

book_titles = [
    "1984",
    "To Kill a Mockingbird",
    "The Hobbit",
    "Dune",
    "The Great Gatsby",
    "The Catcher in the Rye",
    "The Lord of the Rings",
    "The Martian",
    "Jurassic Park",
    "The Hunger Games",
    "The Da Vinci Code",
    "Pride and Prejudice",
    "Dracula",
    "Frankenstein",
    "The Shining",
    "Harry Potter and the Sorcerer's Stone",
    "The Name of the Wind",
    "Mistborn",
    "The Road",
    "Ready Player One"
]

authors = [
    "George Orwell",
    "Harper Lee",
    "J.R.R. Tolkien",
    "Frank Herbert",
    "F. Scott Fitzgerald",
    "J.D. Salinger",
    "J.R.R. Tolkien",
    "Andy Weir",
    "Michael Crichton",
    "Suzanne Collins",
    "Dan Brown",
    "Jane Austen",
    "Bram Stoker",
    "Mary Shelley",
    "Stephen King",
    "J.K. Rowling",
    "Patrick Rothfuss",
    "Brandon Sanderson",
    "Cormac McCarthy",
    "Ernest Cline"
]

genres = [
    "Dystopian",
    "Classic",
    "Fantasy",
    "Science Fiction",
    "Classic",
    "Classic",
    "Fantasy",
    "Science Fiction",
    "Science Fiction",
    "Young Adult",
    "Mystery",
    "Romance",
    "Horror",
    "Horror",
    "Horror",
    "Fantasy",
    "Fantasy",
    "Fantasy",
    "Post-Apocalyptic",
    "Science Fiction"
]

publication_years = [
    1949,
    1960,
    1937,
    1965,
    1925,
    1951,
    1954,
    2011,
    1990,
    2008,
    2003,
    1813,
    1897,
    1818,
    1977,
    1997,
    2007,
    2006,
    2006,
    2011
]

isbns = [
    "978-0-45-152493-5",  
    "978-0-06-093546-7",  
    "978-0-54-792822-7", 
    "978-0-44-117271-9", 
    "978-0-74-327356-5",  
    "978-0-31-676948-8",  
    "978-0-61-864015-7",  
    "978-0-55-341802-6",  
    "978-0-34-553898-7",  
    "978-0-43-902348-1",  
    "978-0-30-747427-8",  
    "978-0-14-143951-8",  
    "978-0-14-143984-6",  
    "978-0-14-143947-1",  
    "978-0-30-774365-7",  
    "978-0-59-035342-7",  
    "978-0-75-640474-1",  
    "978-0-76-535038-1",  
    "978-0-30-738789-9",  
    "978-0-30-788744-3",  
]

"""
for name in member_names:
    library.register_member(name)

for title, author, pub, genre, isbn in zip(book_titles, authors, publication_years, genres, isbns):
    library.add_book(title, author, pub, genre, isbn)
"""