import json
import os
import tkinter as tk
from tkinter import messagebox

# -------------------------------
# Data Handling and User Class
# -------------------------------
DATA_FILE = "data.json"

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.transactions = []
        self.budget = 0

    def add_income(self, amount, source):
        self.transactions.append({"type": "income", "amount": amount, "source": source})

    def add_expense(self, amount, category, description):
        self.transactions.append({"type": "expense", "amount": amount, "category": category, "description": description})

    def view_report(self):
        report = ""
        tincome = 0
        texpense = 0
        expense_category = {}

        for txn in self.transactions:
            if txn['type'] == 'income':
                tincome += txn['amount']
            elif txn['type'] == 'expense':
                texpense += txn['amount']
                expense_category[txn['category']] = expense_category.get(txn['category'], 0) + txn['amount']

        saving = tincome - texpense
        report += f"Total Income: ${tincome:.2f}\n"
        report += f"Total Expenses: ${texpense:.2f}\n"
        report += f"Net Savings: ${saving:.2f}\n\n"

        report += "Top 3 Expense Categories:\n"
        top_expense_categories = sorted(expense_category.items(), key=lambda x: x[1], reverse=True)[:3]
        for category, amount in top_expense_categories:
            report += f"{category}: ${amount:.2f}\n"
        return report

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "transactions": self.transactions,
            "budget": self.budget
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], data["password"])
        user.transactions = data.get("transactions", [])
        user.budget = data.get("budget", 0)
        return user

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return {username: User.from_dict(user_data) for username, user_data in data.items()}
    except FileNotFoundError:
        return {}

def save_data(users):
    with open(DATA_FILE, "w") as file:
        json.dump({u: user.to_dict() for u, user in users.items()}, file)

users = load_data()
current_user = None

# -------------------------------
# GUI Logic
# -------------------------------
def show_register_window():
    reg_win = tk.Toplevel()
    reg_win.title("Register")
    reg_win.geometry("300x200")

    tk.Label(reg_win, text="Username").pack(pady=5)
    username_entry = tk.Entry(reg_win)
    username_entry.pack()

    tk.Label(reg_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(reg_win, show="*")
    password_entry.pack()

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[username] = User(username, password)
            save_data(users)
            messagebox.showinfo("Success", f"User '{username}' registered!")
            reg_win.destroy()

    tk.Button(reg_win, text="Register", command=register).pack(pady=10)

def show_login_window():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username].password == password:
            current_user = users[username]
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            login_win.destroy()
            show_user_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    tk.Button(login_win, text="Login", command=login).pack(pady=10)

def show_user_menu():
    menu_win = tk.Toplevel()
    menu_win.title("Main Menu")
    menu_win.geometry("400x300")

    tk.Label(menu_win, text=f"Welcome, {current_user.username}", font=("Arial", 14)).pack(pady=10)

    def add_income():
        income_win = tk.Toplevel()
        income_win.title("Add Income")

        tk.Label(income_win, text="Amount").pack()
        amount_entry = tk.Entry(income_win)
        amount_entry.pack()

        tk.Label(income_win, text="Source").pack()
        source_entry = tk.Entry(income_win)
        source_entry.pack()

        def save_income():
            amount = float(amount_entry.get())
            source = source_entry.get()
            current_user.add_income(amount, source)
            save_data(users)
            messagebox.showinfo("Success", "Income added!")
            income_win.destroy()

        tk.Button(income_win, text="Add Income", command=save_income).pack(pady=10)

    def add_expense():
        expense_win = tk.Toplevel()
        expense_win.title("Add Expense")

        tk.Label(expense_win, text="Amount").pack()
        amount_entry = tk.Entry(expense_win)
        amount_entry.pack()

        tk.Label(expense_win, text="Category").pack()
        category_entry = tk.Entry(expense_win)
        category_entry.pack()

        tk.Label(expense_win, text="Description").pack()
        desc_entry = tk.Entry(expense_win)
        desc_entry.pack()

        def save_expense():
            amount = float(amount_entry.get())
            category = category_entry.get()
            description = desc_entry.get()
            current_user.add_expense(amount, category, description)
            save_data(users)
            messagebox.showinfo("Success", "Expense added!")
            expense_win.destroy()

        tk.Button(expense_win, text="Add Expense", command=save_expense).pack(pady=10)

    def view_report():
        report = current_user.view_report()
        messagebox.showinfo("Financial Report", report)

    tk.Button(menu_win, text="Add Income", command=add_income).pack(pady=5)
    tk.Button(menu_win, text="Add Expense", command=add_expense).pack(pady=5)
    tk.Button(menu_win, text="View Report", command=view_report).pack(pady=5)
    tk.Button(menu_win, text="Logout", command=menu_win.destroy).pack(pady=10)

def main_ui():
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    root.geometry("400x300")

    tk.Label(root, text="Welcome to Personal Finance Tracker!", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Register", width=20, command=show_register_window).pack(pady=10)
    tk.Button(root, text="Login", width=20, command=show_login_window).pack(pady=10)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_ui()
