from database import init_db, add_category, add_transaction, InvalidTransactionError

def main():
    init_db()
    while True:
        print("\n--- Expense Tracker / Budget Manager ---")
        print("1. Add Category")
        print("2. Add Transaction")
        print("3. Exit")
        choice = input("Select an option: ")

        try:
            if choice == "1":
                name = input("Enter category name: ")
                limit = float(input("Enter monthly budget limit: "))
                add_category(name, limit)
                print("Category added successfully!")
                
            elif choice == "2":
                t_type = input("Type (Income/Expense): ").capitalize()
                amount = float(input("Enter amount: "))
                cat_id = int(input("Enter Category ID: "))
                date = input("Enter date (YYYY-MM-DD): ")
                
                add_transaction(t_type, amount, cat_id, date)
                print("Transaction recorded successfully!")
                
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number for amounts/IDs.")
        except InvalidTransactionError as e:
            print(f"Validation Error: {e}")

if __name__ == "__main__":
    main()
