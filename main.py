import json

#with open('libraryExample.json') as file:
#    library = json.load(file)

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
JSON_FILE = "libraryExample.json"


def read_library_from_json():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def write_library_to_json(library_data):
    with open(JSON_FILE, "w") as file:
        json.dump(library_data, file, indent=4)

library = read_library_from_json()

@app.get("/books")
async def root(isbn = None, test = None):
    #return f"ISBN is: {isbn}, Test is: {test}"
    return library

@app.get("/books/{isbn_number}")
async def get_book_by_isbn(isbn_number: str):
    if isbn_number in library:
        return library[isbn_number]
    else:
        return "Book not found."

@app.delete("/books/{isbn_number}")
async def delete_book_by_isbn(isbn_number: str):
    if isbn_number in library:
        del library[isbn_number]
        return f"Book with ISBN {isbn_number} has been deleted."
    else:
        return "Book does not exist."

def retrieve_books():
    return library

def get_book_isbn(isbn_key):
    return library[isbn_key]['isbn']

def get_book_title(title_key):
    return library[title_key]['title']

def print_book(book_info):
    if not book_info:
        print("Book not found.")
        return
    print (f"Title: {book_info['title']}")
    print (f"Author: {book_info['author']}")
    print (f"ISBN: {book_info['isbn']}")
    print (f"Published Date: {book_info['Published date']}")
    print (f"Genre(s): {book_info['genre']}")
    print(f"Available: {book_info['available']}")

def print_library_book_summary():
    for book_key in library.keys():
        book = library[book_key]
        print(f"Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, Published Date: {book['Published date']}")


def new_book(isbn_key, title, author, isbn, published_date, genre, available):
    library[isbn_key] = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "Published date": published_date,
        "genre": genre,
        "available": available
    }

def remove_book(isbn_key, title, isbn, published_date, genre, available):
    if isbn_key in library:
        del library[isbn_key]
        print(f"Book '{title}' removed from the library.")
    else:
        print(f"Book '{title}' not found in the library.")

def remove_book_by_isbn(isbn_key):
    if isbn_key in library:
        del library[isbn_key]
        print(f"Book with the ISBN '{isbn_key}' was removed from the library.")
    else:
        print(f"Book with the ISBN '{isbn_key}' was not found in the library.")

def save_library_to_json():
    with open("libraryExample.json", "w") as file:
        json.dump(library, file)

def sort_books_by_title():
    sorted_books = sorted(library.items(), key=lambda sorted_books: sorted_books[1]['title'])
    return dict(sorted_books)

def reverse_sort_books_by_title():
    reverse_sorted_books = sorted(library.items(), key=lambda reverse_sorted_books: reverse_sorted_books[1]['title'], reverse=True)
    return dict(reverse_sorted_books)

def main():
    # print("Hello from fastapi-example!")
    for book_key in library.keys():
        print(book_key)

    for book_key in library.keys():
        isbn = get_book_isbn(book_key)
        print(f"\nISBN lookup: {isbn}")
        print_book(library[book_key])

    for book_key in library.keys():
        print(f"Book title: {get_book_title(book_key)}")

    print("\nLibrary Book Summary:")
    print_library_book_summary()

    new_isbn = "978-1-78953-123-4"
    print(f"\nNew book entry for {new_isbn}:")
    new_book(new_isbn, "Docker Deep Dive", "Nigel Poulton", new_isbn, "2020-01-01", ["Technology", "Programming"], True)
    #remove_book(new_isbn, "Docker Deep Dive", new_isbn, "2020-01-01", ["Technology", "Programming"], True)
    #remove_book_by_isbn(new_isbn)

    sorted_books = sort_books_by_title()
    print("\nSorted Books by Title:")
    for book_key in sorted_books.keys():
        print_book(sorted_books[book_key])
        print()

    reverse_sorted_books = reverse_sort_books_by_title()
    print("\nReverse Sorted Books by Title:")
    for book_key in reverse_sorted_books.keys():
        print_book(reverse_sorted_books[book_key])
        print()

    save_library_to_json()
if __name__ == "__main__":
    main()