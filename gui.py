import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app import CSV, plot_transactions
from datetime import datetime
import pandas as pd

# Initialize CSV file
CSV.initialize_csv()

def add_transaction():
    date = date_entry.get_date().strftime(CSV.FORMAT)
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
    update_latest_transactions()

def view_transactions():
    start_date = start_date_entry.get_date().strftime(CSV.FORMAT)
    end_date = end_date_entry.get_date().strftime(CSV.FORMAT)

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

def update_latest_transactions():
    df = pd.read_csv(CSV.CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors='coerce')
    df = df.sort_values(by="date", ascending=False).head(10)  # Get latest 10 transactions
    latest_transactions.delete(*latest_transactions.get_children())
    for index, row in df.iterrows():
        latest_transactions.insert("", "end", values=(row["date"].strftime(CSV.FORMAT), row["amount"], row["category"], row["description"]))

root = tk.Tk()
root.title('Finance Tracker')
root.iconbitmap("icon.ico")
root.geometry("700x900")
root.configure(bg='#D3D3D3')  # Light gray background

# Calculate window size and position to make it centered
window_width = 700
window_height = 900
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create style for ttk elements
style = ttk.Style()
style.theme_use('clam')  # Set theme
style.configure('TNotebook.Tab', font=('Arial', 14), padding=[20, 10], background='#A9A9A9')  # Dark gray
style.map('TNotebook.Tab', background=[('selected', '#696969')])  # Dim gray for selected tab
style.configure('TButton', font=('Arial', 12), padding=10, background='#A9A9A9')
style.configure('TLabel', font=('Arial', 12), padding=10, background='#D3D3D3')
style.configure('TEntry', font=('Arial', 12), fieldbackground='#F0F0F0', background='#C0C0C0')  # Light gray
style.configure('Treeview.Heading', font=('Arial', 12), background='#A9A9A9')
style.configure('Treeview', font=('Arial', 12), rowheight=30, background='#F0F0F0', fieldbackground='#F0F0F0')

# Create Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Add Transaction Frame
add_frame = ttk.Frame(notebook, padding="20", style="TFrame")
notebook.add(add_frame, text="Add Transaction")

ttk.Label(add_frame, text="Date (dd-mm-yyyy)").grid(row=0, column=0, pady=10, sticky="e", padx=30)
date_entry = DateEntry(add_frame, date_pattern="dd-mm-yyyy", width=27, background='darkgray', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1, pady=10, sticky="w")

ttk.Label(add_frame, text="Amount").grid(row=1, column=0, pady=10, sticky="e", padx=30)
amount_entry = ttk.Entry(add_frame, width=30)
amount_entry.grid(row=1, column=1, pady=10, sticky="w")

ttk.Label(add_frame, text="Category").grid(row=2, column=0, pady=10, sticky="e", padx=30)
category_var = tk.StringVar()
category_menu = ttk.Combobox(add_frame, textvariable=category_var, values=("Income", "Expense"), width=28)
category_menu.grid(row=2, column=1, pady=10, sticky="w")

ttk.Label(add_frame, text="Description").grid(row=3, column=0, pady=10, sticky="e", padx=30)
description_entry = ttk.Entry(add_frame, width=30)
description_entry.grid(row=3, column=1, pady=10, sticky="w")

ttk.Button(add_frame, text="Add", command=add_transaction).grid(row=4, columnspan=2, pady=20)

# View Transactions Frame
view_frame = ttk.Frame(notebook, padding="20")
notebook.add(view_frame, text="View Transactions")

ttk.Label(view_frame, text="Start Date (dd-mm-yyyy)").grid(row=0, column=0, pady=10, sticky="e", padx=30)
start_date_entry = DateEntry(view_frame, date_pattern="dd-mm-yyyy", width=27, background='darkgray', foreground='white', borderwidth=2)
start_date_entry.grid(row=0, column=1, pady=10, sticky="w")

ttk.Label(view_frame, text="End Date (dd-mm-yyyy)").grid(row=1, column=0, pady=10, sticky="e", padx=30)
end_date_entry = DateEntry(view_frame, date_pattern="dd-mm-yyyy", width=27, background='darkgray', foreground='white', borderwidth=2)
end_date_entry.grid(row=1, column=1, pady=10, sticky="w")

ttk.Button(view_frame, text="View", command=view_transactions).grid(row=2, columnspan=2, pady=20)

# Latest Transactions Frame
latest_transactions_frame = ttk.Frame(root, padding="20")
latest_transactions_frame.pack(pady=10, fill="both", expand=True)

ttk.Label(latest_transactions_frame, text="Latest Transactions", font=('Arial', 14, 'bold')).pack(pady=10)

columns = ("Date", "Amount", "Category", "Description")
latest_transactions = ttk.Treeview(latest_transactions_frame, columns=columns, show="headings")
for col in columns:
    latest_transactions.heading(col, text=col)
    latest_transactions.column(col, minwidth=0, width=150)

latest_transactions.pack(fill="both", expand=True)
update_latest_transactions()

root.mainloop()
