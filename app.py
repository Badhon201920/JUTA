import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/order', methods=['POST'])
def order():
    # Retrieve form data
    name = request.form['name']
    card_number = request.form['card-number']
    address = request.form['address']
    quantity = request.form['quantity']

    # Save data to the database
    print("Saving data to the database...")
    save_to_database(name, card_number, address, quantity)

    return 'Order successful!'

def save_to_database(name, card_number, address, quantity):
    # Check if the database file exists, if not, create it
    if not os.path.exists('order.db'):
        print("Database file does not exist. Creating it...")
        create_database()

    # Connect to SQLite database
    try:
        conn = sqlite3.connect('order.db')
        print("Database connection established.")
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        return

    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_data
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        card_number TEXT,
                        address TEXT,
                        quantity INTEGER)''')

    # Insert data into the table
    cursor.execute('''INSERT INTO order_data (name, card_number, address, quantity)
                      VALUES (?, ?, ?, ?)''', (name, card_number, address, quantity))

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Data saved to the database.")

def create_database():
    # Connect to SQLite database and close it to create the file
    try:
        conn = sqlite3.connect('order.db')
        print("Database file created.")
    except sqlite3.Error as e:
        print("Error creating the database file:", e)
        return
    conn.close()

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
