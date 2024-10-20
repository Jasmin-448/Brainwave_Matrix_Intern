class ATM:
    def __init__(self, pin, balance=0):
        self.pin = pin
        self.balance = balance
        self.transaction_history = []  

    def check_pin(self, entered_pin):
        return entered_pin == self.pin

    def check_balance(self):
        return f"Your current balance is: ₹{self.balance}"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ₹{amount}") 
            return f"₹{amount} deposited successfully! New balance: ₹{self.balance}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance."
        elif amount > 0:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: ₹{amount}") 
            return f"₹{amount} withdrawn successfully! New balance: ₹{self.balance}"
        return "Invalid withdrawal amount."

    def display_transaction_history(self):
        if not self.transaction_history:
            return "No transactions found."
        return "\n".join(self.transaction_history)


def atm_interface():
    my_atm = ATM(pin="1234", balance=10000)
    print("----- Welcome to Python Bank ATM -----")
    for attempt in range(3):
        entered_pin = input("Please enter your 4-digit PIN: ")
        if my_atm.check_pin(entered_pin):
            print("PIN verified successfully!")
            break
        else:
            print(f"Incorrect PIN. {2 - attempt} attempts remaining.")
            if attempt == 2:
                print("Too many failed attempts. Exiting...")
                return  

    while True:
        try:
            print("\nOptions:")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Transaction History")
            print("5. Exit")

            choice = input("Please select an option (1-5): ")

            if choice == '1':
                print(my_atm.check_balance())

            elif choice == '2':
                try:
                    deposit_amount = float(input("Enter amount to deposit: ₹"))
                    print(my_atm.deposit(deposit_amount))
                except ValueError:
                    print("Invalid input. Please enter a valid amount.")

            elif choice == '3':
                try:
                    withdraw_amount = float(input("Enter amount to withdraw: ₹"))
                    print(my_atm.withdraw(withdraw_amount))
                except ValueError:
                    print("Invalid input. Please enter a valid amount.")

            elif choice == '4':
                print("\nTransaction History:")
                print(my_atm.display_transaction_history())

            elif choice == '5':
                print("Thank you for using Python Bank ATM. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\nOperation interrupted. Please try again or exit by choosing option 5.")
            continue


if __name__ == "__main__":
    atm_interface()
