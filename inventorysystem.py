import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox

# Database setup
def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')

    # Create Products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        quantity INTEGER,
                        price REAL
                    )''')
    conn.commit()
    conn.close()

setup_database()

# User Authentication Functions
def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "User created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    return False

# Inventory Management Functions
def add_product(name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

def edit_product(product_id, name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def view_products():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def low_stock_alert(threshold=5):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < ?", (threshold,))
    low_stock_items = cursor.fetchall()
    conn.close()
    return low_stock_items

# GUI Functions
def display_products():
    products = view_products()
    product_list.delete(0, tk.END)
    for product in products:
        product_list.insert(tk.END, f"ID: {product[0]}, Name: {product[1]}, Qty: {product[2]}, Price: ${product[3]:.2f}")

def add_product_gui():
    name = name_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    add_product(name, quantity, price)
    display_products()
    messagebox.showinfo("Success", "Product added successfully!")

def delete_product_gui():
    try:
        product_id = int(product_id_entry.get())
        delete_product(product_id)
        display_products()
        messagebox.showinfo("Success", "Product deleted successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid Product ID.")

# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()
    if login_user(username, password):
        messagebox.showinfo("Login Success", "Welcome!")
        login_frame.pack_forget()
        inventory_frame.pack()
        display_products()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# Register Function
def register():
    username = username_entry.get()
    password = password_entry.get()
    create_user(username, password)

# Main Application
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("600x400")

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

tk.Label(login_frame, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

tk.Label(login_frame, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, pady=10)
register_button = tk.Button(login_frame, text="Register", command=register)
register_button.grid(row=2, column=1, pady=10)

# Inventory Management Frame
inventory_frame = tk.Frame(root)

# Product List
product_list = tk.Listbox(inventory_frame, width=50)
product_list.grid(row=0, column=0, columnspan=4, padx=20, pady=10)

# Add Product Section
tk.Label(inventory_frame, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(inventory_frame)
name_entry.grid(row=1, column=1)

tk.Label(inventory_frame, text="Quantity").grid(row=1, column=2)
quantity_entry = tk.Entry(inventory_frame)
quantity_entry.grid(row=1, column=3)

tk.Label(inventory_frame, text="Price").grid(row=2, column=0)
price_entry = tk.Entry(inventory_frame)
price_entry.grid(row=2, column=1)

add_button = tk.Button(inventory_frame, text="Add Product", command=add_product_gui)
add_button.grid(row=2, column=2, columnspan=2, pady=10)

# Delete Product Section
tk.Label(inventory_frame, text="Product ID").grid(row=3, column=0)
product_id_entry = tk.Entry(inventory_frame)
product_id_entry.grid(row=3, column=1)

delete_button = tk.Button(inventory_frame, text="Delete Product", command=delete_product_gui)
delete_button.grid(row=3, column=2, columnspan=2, pady=10)

root.mainloop()
