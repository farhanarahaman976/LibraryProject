import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# ===== Database Setup =====
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(member_id) REFERENCES members(id)
)
''')
conn.commit()

# ===== Functions =====
def add_book():
    title = simpledialog.askstring("Add Book", "Enter book title:")
    author = simpledialog.askstring("Add Book", "Enter author name:")
    if title and author:
        cursor.execute("INSERT INTO books (title, author, available) VALUES (?, ?, 1)", (title, author))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")

def search_book():
    keyword = simpledialog.askstring("Search Book", "Enter book title or author:")
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    if results:
        result_str = ""
        for book in results:
            status = "Available" if book[3] == 1 else "Issued"
            result_str += f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}\n"
        messagebox.showinfo("Search Results", result_str)
    else:
        messagebox.showinfo("Search Results", "No books found!")

def issue_book():
    book_id = simpledialog.askinteger("Issue Book", "Enter Book ID:")
    member_id = simpledialog.askinteger("Issue Book", "Enter Member ID:")
    cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if book and book[0] == 1:
        cursor.execute("INSERT INTO issued_books (book_id, member_id) VALUES (?, ?)", (book_id, member_id))
        cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book issued successfully!")
    else:
        messagebox.showerror("Error", "Book not available!")

def return_book():
    book_id = simpledialog.askinteger("Return Book", "Enter Book ID:")
    cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
    conn.commit()
    messagebox.showinfo("Success", "Book returned successfully!")

def add_member():
    name = simpledialog.askstring("Add Member", "Enter member name:")
    if name:
        cursor.execute("INSERT INTO members (name) VALUES (?)", (name,))
        conn.commit()
        messagebox.showinfo("Success", "Member added successfully!")

def show_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    if members:
        result_str = "\n".join([f"ID: {m[0]}, Name: {m[1]}" for m in members])
        messagebox.showinfo("Members", result_str)
    else:
        messagebox.showinfo("Members", "No members found!")

def show_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        result_str = ""
        for b in books:
            status = "Available" if b[3] == 1 else "Issued"
            result_str += f"ID: {b[0]}, Title: {b[1]}, Author: {b[2]}, Status: {status}\n"
        messagebox.showinfo("All Books", result_str)
    else:
        messagebox.showinfo("All Books", "No books found!")

def show_available_books():
    cursor.execute("SELECT * FROM books WHERE available = 1")
    books = cursor.fetchall()
    if books:
        result_str = ""
        for b in books:
            result_str += f"ID: {b[0]}, Title: {b[1]}, Author: {b[2]}, Status: Available\n"
        messagebox.showinfo("Available Books", result_str)
    else:
        messagebox.showinfo("Available Books", "No available books!")

def issued_books_list():
    cursor.execute('''
        SELECT books.title, members.name 
        FROM issued_books
        JOIN books ON issued_books.book_id = books.id
        JOIN members ON issued_books.member_id = members.id
    ''')
    records = cursor.fetchall()
    if records:
        result_str = ""
        for r in records:
            result_str += f"Book: {r[0]} → Issued to: {r[1]}\n"
        messagebox.showinfo("Issued Books", result_str)
    else:
        messagebox.showinfo("Issued Books", "No books are currently issued!")

# ===== Tkinter UI =====
root = tk.Tk()
root.title("Library Management System")
root.geometry("400x500")

title_label = tk.Label(root, text="Library Management System", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

btn_add_book = tk.Button(root, text="Add Book", width=25, command=add_book)
btn_add_book.pack(pady=5)

btn_search_book = tk.Button(root, text="Search Book", width=25, command=search_book)
btn_search_book.pack(pady=5)

btn_issue_book = tk.Button(root, text="Issue Book", width=25, command=issue_book)
btn_issue_book.pack(pady=5)

btn_return_book = tk.Button(root, text="Return Book", width=25, command=return_book)
btn_return_book.pack(pady=5)

btn_add_member = tk.Button(root, text="Add Member", width=25, command=add_member)
btn_add_member.pack(pady=5)

btn_show_members = tk.Button(root, text="Show Members", width=25, command=show_members)
btn_show_members.pack(pady=5)

btn_show_books = tk.Button(root, text="Show All Books", width=25, command=show_books)
btn_show_books.pack(pady=5)

btn_show_available_books = tk.Button(root, text="Show Available Books", width=25, command=show_available_books)
btn_show_available_books.pack(pady=5)

btn_issued_books = tk.Button(root, text="Issued Books List", width=25, command=issued_books_list)
btn_issued_books.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", width=25, command=root.quit)
btn_exit.pack(pady=10)

root.mainloop()
