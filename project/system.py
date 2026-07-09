import os, json, time

from models.library import Library

library = Library()

def color_text(text, color = "end"):
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
    while True:
        print("===== Main Menu =====")
        print("1. Login Member")
        print("2. Login Admin")
        print("3. Register Member")
        print("4. Register Admin")
        print("5. Exit\n")
        
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError, ValueError):
            print(color_text("\nIncorrect input type, please try again\n", "red"))
            continue

        int(user_input)
        print(type(user_input))

        if user_input == 1:
            try:
                username = input("Input your accounts name: ").strip()
                user_id = int(input("Input your account ID: "))
            except (KeyboardInterrupt, EOFError, ValueError):
                print(color_text("\nIncorrect input type, please try again\n", "red"))
                continue




def member_menu():
    print("===== Member Menu =====")

def admin_menu():
    print("===== Admin Menu =====")

def login(username, id):
    pass

def save(data, filepath):
    pass

def load(filepath):
    pass 



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


main_menu()