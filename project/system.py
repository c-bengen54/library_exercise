import time
import bcrypt
from models.library import Library, access

code, expiration = access

library = Library()

def get_input(question:str, conversion:bool = False) -> str | int:
    """
    Gets user input and returns the value entered

    Parameters:
        question (str):
            The flavor text meant to tell the user
            what they're meant to answer
        
        conversion (bool):
            The flag which determines whether the input will be 
            converted to an integer value.
            - Should only be used if the input type is expected to be an integer value
    
    Returns:
        str | int:
            Returns the string value of what the user inputted,
            or an integer if the input was converted

    """
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
            except (KeyboardInterrupt, EOFError):
                print(color_text("\nIncorrect input type, please try again\n", "red"))
                continue
        return user_input

def color_text(text:str, color:str = "end") -> str:
    """
    Return a colorized string of text.

    Parameters:
        text (str):
            The string to be colored

        color (str):
            The color you wish to color the text as, defaults to end
            Supported colors include:
            - bold
            - red
            - green
            - yellow
            - blue
            - magenta
            - cyan
            - white
            - italic
            - end
    Returns:
        str:
            A colorized string
    """
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
            pass

        elif user_input == 3:
            member_name = get_input("\nInput requested name: ")
            m_first_name = get_input("\nInput your first name: ")
            m_last_name = get_input("\nInput your last name: ")
            m_email = get_input("\nInput your email: ")
            password = get_input("\nInput your password: ")
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            u_id = library.register_user(member_name,m_first_name, m_last_name, m_email, password, "member")
            print("\nAccount registered", color_text(f"\n{member_name} ID: {u_id}", "green"))

        elif user_input == 4:
            admin_name = get_input("\nInput requested name: ")
            a_first_name = get_input("\nInput your first name: ")
            a_last_name = get_input("\nInput your last name: ")
            a_email = get_input("\nInput your email: ")
            password = get_input("\nInput your password: ")
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            admin_code = get_input("\nInput admin registration code: ", True)

            u_id = library.register_user(admin_name, a_first_name, a_last_name, a_email, password, "admin", admin_code)
            print("\nAdmin registered", color_text(f"\n{admin_name} ID: {u_id}", "green"))

        elif user_input ==5:
            print(color_text("\nExiting program...", "yellow"))
            time.sleep(2)
            print(color_text("\n- Have a wonderful day!!\n", "cyan"))
            break

        else:
            print(color_text("\nInputted option either not in menu, or incorrect input type. \nPlease try again.\n", "red"))
            time.sleep(2)

def member_login():
    username = get_input("\nUsername: ")
    user_id = get_input("\nID: ", True)
    password = get_input("\nPassword: ")
    password = password.encode("utf-8")

    user = library.select("users", "user_id", user_id)

    if user is None:
            print(color_text("\nNo user found.\n", "red"))
            return

    if user[1] != user_id:
        print(color_text("\nInvalid user ID.\n", "red"))
        return

    if user[2] != username:
        print(color_text("\nInvalid username.\n", "red"))
        return

    stored_hash = bytes.fromhex(user[6][2:])

    if not bcrypt.checkpw(password, stored_hash):
        print(color_text("\nInvalid password.\n", "red"))
        return

    print(color_text("\nEntering member menu.....", "yellow"))
    time.sleep(2)
    member_menu()
    return

def admin_login():
    username = get_input("\nUsername: ")
    admin_id = get_input("\nAdmin ID: ", True)
    password = get_input("\nPassword: ")
    password = password.encode("utf-8")
    access_code = get_input("\nAccess Code: ", True)

    admin = library.select("users", "user_id", admin_id)

    if admin is None :
        print(color_text("\nNo user found.\n", "red"))
        return
    
    if access_code != code:
        print(color_text("\nInvalid access code.\n", "red"))
        return
    
    if admin[2] != username:
        print(color_text("\nInvalid username.\n", "red"))
        return
    
    if admin_id != admin[1]:
        print(color_text("\nInvalid admin ID.\n", "red"))
        return

    stored_hash = bytes.fromhex(admin[6][2:])

    if not bcrypt.checkpw(password, stored_hash):
        print(color_text("\nInvalid password.\n", "red"))
        return 

    print(color_text("\nEntering admin menu.....", "yellow"))
    time.sleep(2)
    admin_menu()
    return
    
def member_menu():
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
            identity = get_input("Input your user ID > ", True)
            title = get_input("Input title you wish to check out > ")
            book = library.search_by_title(title)

            if book is None:
                print(color_text("\nBook not found.\n", "red"))
                continue

            library.check_out(identity, book[0])
            print(color_text("Title sucessfully checked out", "green"))
            
        elif user_input == 2:
            identity = get_input("Input your user ID > ", True)
            title = get_input("Input title you wish to reserve > ")
            book = library.search_by_title(title)

            if book is None:
                print(color_text("\nBook not found.\n", "red"))
                continue

            library.reserve_book(identity, book[0])
            print(color_text("Title sucessfully reserved", "green"))
             

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
            print(color_text("Functionality not yet implemented", "red"))

        elif user_input == 7:
            print(color_text("Functionality not yet implemented", "red"))

        elif user_input == 8:
            print(color_text("Exiting member menu.....", "yellow"))
            time.sleep(2)
            break

        else:
            continue

def admin_menu():    
    while True:
        print("\n===== Admin Menu =====")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Update User Name")
        print("4. Update User ID")
        print("5. View Global Log")
        print("6. Exit\n")

        user_input  = get_input("> ", True)

        if user_input == 1:
            title = get_input("Input title > ")
            author = get_input("Input books author > ")
            publication = get_input("Input Publication Year > ", True)
            genre = get_input("Input book genre > ")
            isbn = get_input("Input the books ISBN code\n(Strict form - ISBN-13: XXX-X-XX-XXXXXX-X) ISBN-10: X-XXX-XXXXX-X\n>")
            library.add_book(title, author, publication, genre, isbn)
            print(color_text("\nBook added to catalogue successfully", "green"))
            

        elif user_input == 2:
            book_id = get_input("Input the book database id > ", True)
            library.remove_book(book_id)
            print(color_text("\nBook removed from catalogue successfully", "green"))
            

        elif user_input == 3:
            member_id = get_input("Input user ID > ")
            requested_name = get_input("Input requested name > ")
            member = library.select("users", "user_id", member_id)
            member_name = member[2]
            library.update_user(member_name, requested_name, member_id)
            print(color_text("\nName updated successfully", "green"))
            

        elif user_input == 4:
            member_id = get_input("Input users ID > ")
            requested_id = get_input("Input new ID > ", True)
            library.update_user("user_id", requested_id, member_id)
            print(color_text("\nUser's ID updated successfully", "green"))
            
        elif user_input == 5:
            library.view_logs()
            time.sleep(2)

        elif user_input == 6:
            print(color_text("Exiting admin menu.....", "yellow"))
            time.sleep(2)
            break

        else:
            continue