import re
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('contacts.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contact
             (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

# Functions for CRUD operations
def add_contact():
    name = name_entry.get()
    email = email_entry.get()
    if name and email:
        if valideEmail(email) and valideNom(name):
            c.execute("INSERT INTO contact (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            load_contacts()
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter valide name and email")
    else:
        messagebox.showwarning("Input Error", "Please enter both name and email")

def update_contact():
    selected_item = contacts_listbox.curselection()
    if selected_item:
        contact_id = contacts_listbox.get(selected_item)[0]
        new_name = name_entry.get()
        new_email = email_entry.get()
        if new_name and new_email:
            if valideEmail(new_email) and valideNom(new_name):
                c.execute("UPDATE contact SET name = ?, email = ? WHERE id = ?", (new_name, new_email, contact_id))
                conn.commit()
                load_contacts()
            else:
                messagebox.showwarning("Input Error", "Please enter valide name and email")
        else:
            messagebox.showwarning("Input Error", "Please enter both name and email")

def delete_contact():
    selected_item = contacts_listbox.curselection()
    if selected_item:
        contact_id = contacts_listbox.get(selected_item)[0]
        c.execute("DELETE FROM contact WHERE id = ?", (contact_id,))
        conn.commit()
        load_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete")

def load_contacts():
    contacts_listbox.delete(0, tk.END)
    c.execute("SELECT * FROM contact")
    for row in c.fetchall():
        contacts_listbox.insert(tk.END, row)

def valideEmail(email):
    exEmail = r"[a-zA-Z\._+-]+[0-9]*@[a-z]+\.[a-z]+"
    return re.match(exEmail, email)
def valideNom(nom):
    exNom = r"[A-Z][a-zA-Z]{2,}"
    return re.match(exNom, nom)

# GUI setup
root = tk.Tk()
root.title("Contact Manager")
root.iconbitmap("./python-png.ico")

tk.Label(root, text="Name:", font=('Arial', 20)).grid(row=0, column=0)
name_entry = tk.Entry(root, font=('Arial', 20))
name_entry.grid(row=0, column=1)

tk.Label(root, text="Email:", font=('Arial', 20)).grid(row=1, column=0)
email_entry = tk.Entry(root, font=('Arial', 20))
email_entry.grid(row=1, column=1)

tk.Button(root, text="Add", command=add_contact, font=('Arial', 20)).grid(row=2, column=0)
tk.Button(root, text="Update", command=update_contact, font=('Arial', 20)).grid(row=2, column=1)
tk.Button(root, text="Delete", command=delete_contact, font=('Arial', 20)).grid(row=2, column=2)

contacts_listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=('Arial', 20))
contacts_listbox.grid(row=3, column=0, columnspan=3, sticky="nsew")

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

load_contacts()

root.mainloop()