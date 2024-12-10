import json

# File to store user data
DATA_FILE = "data.json"

# Define a basic User class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.transactions = []  # List to store income and expenses
        self.budget = 0  # Budget limit

    def add_income(self, amount, source):
        # Add income to transactions
        pass

    def add_expense(self, amount, category, description):
        # Add expense to transactions
        pass

    def view_report(self):
        # Generate and display financial report
        pass

# Load data from file
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Register a new user
def register_user(users):
    # Get username and password
    # Create a new User object
    pass

# Login an existing user
def login_user(users):
    # Validate username and password
    pass

# Main menu
def main_menu(user):
    while True:
        print("\nMain Menu")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Report")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            # Call add_income on the user
            pass
        elif choice == "2":
            # Call add_expense on the user
            pass
        elif choice == "3":
            # Call view_report on the user
            pass
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice! Try again.")

# Main program
def main():
    users = load_data()

    while True:
        print("\nWelcome to the Finance Tracker")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_user(users)
        elif choice == "2":
            user = login_user(users)
            if user:
                main_menu(user)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

    save_data(users)

if __name__ == "__main__":
    main()
