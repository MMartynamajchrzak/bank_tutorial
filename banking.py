# Write your code here
import random
import user_dataDB

connection = user_dataDB.connect()
user_dataDB.create_table(connection)


class Bank:

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

    @staticmethod
    def luhn_algorithm(bin_num):

        numbers_map = map(int, bin_num)
        card_num = list(numbers_map)

        new_card_num = []

        for position, num in enumerate(card_num):
            if (position + 1) % 2 != 0:
                num *= 2
            if num > 9:
                num -= 9
            new_card_num.append(num)

        check_difference = (sum(new_card_num) % 10)

        if check_difference == 0:
            checksum = 0
        else:
            checksum = 10 - check_difference

        return checksum

    def create_account(self):
        user_data = {}
        inn_num = "400000"

        ai_num = ''
        for _ in range(9):
            num = random.randint(0, 9)
            ai_num += str(num)

        pin = ''
        for _ in range(4):
            num = random.randint(0, 9)
            pin += str(num)

        bin_num = inn_num + str(ai_num)

        checksum = self.luhn_algorithm(bin_num)

        updated_card_number = bin_num + str(checksum)

        user_data[updated_card_number] = pin
        print("Your card has been created")
        print("Your card number:")
        print(updated_card_number)
        print("Your card PIN:")
        print(pin)

        # storing card_no, pin and balance to database
        user_dataDB.save_data(connection, updated_card_number, pin)
        self.main_menu()

    def balance_func(self):
        print("Balance: ", user_dataDB.balance(connection))
        self.logged_menu()

    def log_out(self):
        print("You have successfully logged out!")
        self.main_menu()

    @staticmethod
    def exit_func():
        print("Bye!")

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
        pin_input = input("Enter your PIN:\n")
        valid_account = False

        if user_dataDB.check_data(connection, account_number, pin_input) > 0:
            valid_account = True

        if valid_account:
            print("You have successfully logged in!")
            self.logged_menu()
        else:
            print("Wrong card number or PIN")
            self.main_menu()


new_client = Bank()
new_client.main_menu()
