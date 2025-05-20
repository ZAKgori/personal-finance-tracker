import json
from tkinter import messagebox
from tkinter import ttk  # Keep this for Treeview
import customtkinter as CTk
from PIL import Image 

# Configure customtkinter appearance
CTk.set_appearance_mode("dark")  # Can be "Dark" or "Light"
CTk.set_default_color_theme("green")  # You can change this to "green", "dark-blue", etc.

img = Image.open('piggybank.png')

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
        report = []
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
        report.append(f"${tincome:.2f}")
        report.append(f"${texpense:.2f}")
        report.append(f"${saving:.2f}")

        top_expense_categories = sorted(expense_category.items(), key=lambda x: x[1], reverse=True)[:3]
        report.append(top_expense_categories)
        return report

    def view_expenses(self):
        return [txn for txn in self.transactions if txn["type"] == "expense"]

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
    reg_win = CTk.CTkToplevel()
    reg_win.title("Register")
    reg_win.geometry("300x200")

    CTk.CTkLabel(reg_win, text="Username").pack(pady=5)
    username_entry = CTk.CTkEntry(reg_win)
    username_entry.pack()

    CTk.CTkLabel(reg_win, text="Password").pack(pady=5)
    password_entry = CTk.CTkEntry(reg_win, show="*")
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

    CTk.CTkButton(reg_win, text="Register", command=register).pack(pady=10)

def show_login_window():
    login_win = CTk.CTkToplevel()
    login_win.title("Login")
    login_win.geometry("300x200")

    CTk.CTkLabel(login_win, text="Username").pack(pady=5)
    username_entry = CTk.CTkEntry(login_win)
    username_entry.pack()

    CTk.CTkLabel(login_win, text="Password").pack(pady=5)
    password_entry = CTk.CTkEntry(login_win, show="*")
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

    CTk.CTkButton(login_win, text="Login", command=login).pack(pady=10)

def show_user_menu():
    menu_win = CTk.CTkToplevel()
    menu_win.title("Main Menu")
    menu_win.geometry("400x400")

    CTk.CTkLabel(menu_win, text=f"Welcome, {current_user.username}", font=("Arial", 16)).pack(pady=10)

    def add_income():
        income_win = CTk.CTkToplevel()
        income_win.title("Add Income")

        CTk.CTkLabel(income_win, text="Amount").pack()
        amount_entry = CTk.CTkEntry(income_win)
        amount_entry.pack()

        CTk.CTkLabel(income_win, text="Source").pack()
        source_entry = CTk.CTkEntry(income_win)
        source_entry.pack()

        def save_income():
            try:
                amount = float(amount_entry.get())
                source = source_entry.get()
                current_user.add_income(amount, source)
                save_data(users)
                messagebox.showinfo("Success", "Income added!")
                income_win.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

        CTk.CTkButton(income_win, text="Add Income", command=save_income).pack(pady=10)

    def add_expense():
        expense_win = CTk.CTkToplevel()
        expense_win.title("Add Expense")

        CTk.CTkLabel(expense_win, text="Amount").pack()
        amount_entry = CTk.CTkEntry(expense_win)
        amount_entry.pack()

        CTk.CTkLabel(expense_win, text="Category").pack()
        category_entry = CTk.CTkEntry(expense_win)
        category_entry.pack()

        CTk.CTkLabel(expense_win, text="Description").pack()
        desc_entry = CTk.CTkEntry(expense_win)
        desc_entry.pack()

        def save_expense():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get()
                description = desc_entry.get()
                current_user.add_expense(amount, category, description)
                save_data(users)
                messagebox.showinfo("Success", "Expense added!")
                expense_win.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

        CTk.CTkButton(expense_win, text="Add Expense", command=save_expense).pack(pady=10)

    def view_report():
        report = current_user.view_report()

        window = CTk.CTkToplevel()
        window.geometry('800x250')
        window.title('Financial Report')

        table = ttk.Treeview(window, columns=('Total income', 'Total expense', 'Net saving', 'Top 3 expense categories'), show='headings')
        table.heading('Total income', text='Total income')
        table.heading('Total expense', text='Total expense')
        table.heading('Net saving', text='Net saving')
        table.heading('Top 3 expense categories', text='Top 3 expense categories')

        top_categories = ", ".join([f"{cat}: ${amt:.2f}" for cat, amt in report[3]])
        table.insert('', 'end', values=(report[0], report[1], report[2], top_categories))
        table.pack(expand=True, fill='both', padx=10, pady=10)

    def view_expenses():
        expenses = current_user.view_expenses()

        windowE = CTk.CTkToplevel()
        windowE.geometry('800x300')
        windowE.title('Expense List')

        etable = ttk.Treeview(windowE, columns=('Amount', 'Category', 'Description'), show='headings')
        etable.heading('Amount', text='Amount')
        etable.heading('Category', text='Category')
        etable.heading('Description', text='Description')

        for txn in expenses:
            etable.insert('', 'end', values=(txn['amount'], txn['category'], txn['description']))

        etable.pack(expand=True, fill='both', padx=10, pady=10)

    CTk.CTkButton(menu_win, text="Add Income", command=add_income).pack(pady=5)
    CTk.CTkButton(menu_win, text="Add Expense", command=add_expense).pack(pady=5)
    CTk.CTkButton(menu_win, text="View Expense", command=view_expenses).pack(pady=5)
    CTk.CTkButton(menu_win, text="View Report", command=view_report).pack(pady=5)
    CTk.CTkButton(menu_win, text="Logout", command=menu_win.destroy).pack(pady=10)

def main_ui():
    root = CTk.CTk()
    root.title("Personal Finance Tracker")
    root.geometry("400x400")

    # Load and display image
    image = CTk.CTkImage(light_image=img, dark_image=img, size=(100, 100))
    CTk.CTkLabel(root, image=image, text="").pack(pady=10)

    CTk.CTkLabel(root, text="Welcome to Personal Finance Tracker!", font=("Arial", 16)).pack(pady=10)
    CTk.CTkButton(root, text="Register", width=200, command=show_register_window).pack(pady=10)
    CTk.CTkButton(root, text="Login", width=200, command=show_login_window).pack(pady=10)
    CTk.CTkButton(root, text="Exit", width=200, command=root.quit).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_ui()
