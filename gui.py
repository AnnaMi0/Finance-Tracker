import tkinter as tk
from tkinter import messagebox
from app import CSV, plot_transactions
from datetime import datetime

# Initialize CSV file
CSV.initialize_csv()

def add_transaction():
    date = date_entry.get()
    amount = amount_entry.get()
    category = category_var.get()
    description = description_entry.get()
    
    if not date or not amount or not category:
        messagebox.showerror("Input Error", "Please fill all the required fields")
        return

    try:
        amount = float(amount)
        datetime.strptime(date, CSV.FORMAT)  # Validate date format
    except ValueError:
        messagebox.showerror("Input Error", "Invalid date or amount format")
        return

    CSV.add_entry(date, amount, category, description)
    messagebox.showinfo("Success", "Transaction added successfully")

def view_transactions():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    if not start_date or not end_date:
        messagebox.showerror("Input Error", "Please provide both start and end dates")
        return

    try:
        datetime.strptime(start_date, CSV.FORMAT)
        datetime.strptime(end_date, CSV.FORMAT)
    except ValueError:
        messagebox.showerror("Input Error", "Invalid date format")
        return

    df = CSV.get_transactions(start_date, end_date)
    if not df.empty:
        plot_transactions(df)

root = tk.Tk()
root.title('Finance Tracker')
root.geometry("600x400")

# Add Transaction Frame
add_frame = tk.Frame(root, padx=10, pady=10)
add_frame.pack(pady=10)

tk.Label(add_frame, text="Add Transaction").grid(row=0, columnspan=2)

tk.Label(add_frame, text="Date (dd-mm-yyyy)").grid(row=1, column=0, pady=5)
date_entry = tk.Entry(add_frame)
date_entry.grid(row=1, column=1, pady=5)

tk.Label(add_frame, text="Amount").grid(row=2, column=0, pady=5)
amount_entry = tk.Entry(add_frame)
amount_entry.grid(row=2, column=1, pady=5)

tk.Label(add_frame, text="Category").grid(row=3, column=0, pady=5)
category_var = tk.StringVar()
category_menu = tk.OptionMenu(add_frame, category_var, "Income", "Expense")
category_menu.grid(row=3, column=1, pady=5)

tk.Label(add_frame, text="Description").grid(row=4, column=0, pady=5)
description_entry = tk.Entry(add_frame)
description_entry.grid(row=4, column=1, pady=5)

tk.Button(add_frame, text="Add", command=add_transaction).grid(row=5, columnspan=2, pady=10)

# View Transactions Frame
view_frame = tk.Frame(root, padx=10, pady=10)
view_frame.pack(pady=10)

tk.Label(view_frame, text="View Transactions").grid(row=0, columnspan=2)

tk.Label(view_frame, text="Start Date (dd-mm-yyyy)").grid(row=1, column=0, pady=5)
start_date_entry = tk.Entry(view_frame)
start_date_entry.grid(row=1, column=1, pady=5)

tk.Label(view_frame, text="End Date (dd-mm-yyyy)").grid(row=2, column=0, pady=5)
end_date_entry = tk.Entry(view_frame)
end_date_entry.grid(row=2, column=1, pady=5)

tk.Button(view_frame, text="View", command=view_transactions).grid(row=3, columnspan=2, pady=10)

root.mainloop()
