# Write your code here
import random


class Bank:

    def __init__(self):
        self.accounts = []
        self.balance = 0

    def main_menu(self):
        options = {'1.': "Create an account", '2.': "Log into account", '3.': "Exit"}
        for item, value in options.items():
            print(item, value)

        choice = int(input())

        if choice == 1:
            self.create_account()
        elif choice == 2:
            self.log_into_account()
        elif choice == 0:
            self.exit_func()

    def create_account(self):
        user_data = {}
        inn_num = "400000"

        ai_num = ''
        for _ in range(10):
            num = random.randint(0, 9)
            ai_num += str(num)

        pin = ''
        for _ in range(4):
            num = random.randint(0, 9)
            pin += str(num)

        card_number = inn_num + str(ai_num)

        user_data[card_number] = pin
        print("Your card has been created")
        print("Your card number:")
        print(int(card_number))
        print("Your card PIN:")
        print(pin)

        self.accounts.append(user_data)
        self.main_menu()
        # store the card_no and pin in array in order to persist the data, so that user can log in any time

    def balance_func(self):
        print("Balance: ", self.balance)
        self.logged_menu()

    def log_out(self):
        print("You have successfully logged out!")
        self.main_menu()

    @staticmethod
    def exit_func():
        print("Bye!")

    # if statement connected with user input --> how will particular no interact with dictionaries key

    def logged_menu(self):
        options = {'1.': "Balance", '2.': "Log out", '0.': "Exit"}
        for item, value in options.items():
            print(item, value)

        choice = int(input())

        if choice == 1:
            self.balance_func()
        elif choice == 2:
            self.log_out()
        elif choice == 0:
            self.exit_func()

    def log_into_account(self):
        account_number = input("Enter account number:\n")
        pin_input = input("Enter yout PIN:\n")
        valid_account = False

        for account_data in self.accounts:
            if account_number in account_data.keys() and pin_input in account_data.values():
                valid_account = True
                break

        if valid_account:
            print("You have successfully logged in!")
            self.logged_menu()
        else:
            print("Wrong card number or PIN")
            self.main_menu()


new_client = Bank()
new_client.main_menu()
