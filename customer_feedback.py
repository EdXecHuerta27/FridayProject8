import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Ensure the feedback table exists
def create_table():
    conn = sqlite3.connect('customer_feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Create the table when the script runs
create_table()

# Function to submit feedback
def submit_feedback():
    name = name_entry.get()
    email = email_entry.get()
    feedback = feedback_entry.get()

    if name and email and feedback:
        conn = sqlite3.connect('customer_feedback.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)', (name, email, feedback))
        conn.commit()
        conn.close()
        messagebox.showinfo('Success', 'Feedback submitted!')
        # Clear input fields after submission
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        feedback_entry.delete(0, tk.END)
    else:
        messagebox.showwarning('Error', 'All fields must be filled out.')

# Function to retrieve feedback with password protection
def retrieve_feedback():
    # Ask for the password through a GUI dialog box
    password = simpledialog.askstring("Password", "Enter password to access feedback:", show='*')
    if password == '12345':  # Replace with your chosen password
        conn = sqlite3.connect('customer_feedback.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM feedback')
        all_entries = cursor.fetchall()
        conn.close()

        # Print feedback entries in the console
        if all_entries:
            print("\n--- Customer Feedback ---")
            for entry in all_entries:
                print(f'ID: {entry[0]}, Name: {entry[1]}, Email: {entry[2]}, Feedback: {entry[3]}')
        else:
            print('No feedback entries found.')
    else:
        print('Access denied. Incorrect password.')

# Create the main GUI window
window = tk.Tk()
window.title('Customer Feedback Application')

# Create and place widgets in the window
tk.Label(window, text='Name').grid(row=0, column=0)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1)

tk.Label(window, text='Email').grid(row=1, column=0)
email_entry = tk.Entry(window)
email_entry.grid(row=1, column=1)

tk.Label(window, text='Feedback').grid(row=2, column=0)
feedback_entry = tk.Entry(window, width=40)
feedback_entry.grid(row=2, column=1)

# Submit button
submit_button = tk.Button(window, text='Submit', command=submit_feedback)
submit_button.grid(row=3, columnspan=2)

# Retrieve button
retrieve_button = tk.Button(window, text='Retrieve Data', command=retrieve_feedback)
retrieve_button.grid(row=4, columnspan=2)

# Start the GUI event loop
window.mainloop()



