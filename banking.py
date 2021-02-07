# Write your code here
import random
import user_dataDB

# creating connection and card table in user_dataDB
connection = user_dataDB.connect()
user_dataDB.create_table(connection)


class Bank:

    def __init__(self):
        self.correct_number = 0
        self.correct_pin = 0

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

    # func for calculating checksum
    @staticmethod
    def luhn_algorithm(bin_num):

        numbers_map = map(int, bin_num)
        card_num = list(numbers_map)

        if len(card_num) > 15:
            del card_num[-1]

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

        # generating account number
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

        # storing card_no, pin and balance in database
        user_dataDB.save_data(connection, updated_card_number, pin)
        self.main_menu()

    def log_into_account(self):
        account_number = input("Enter account number:\n")
        pin_input = input("Enter your PIN:\n")
        valid_account = False

        # if such data are in database = valid account, log in
        if user_dataDB.check_data(connection, account_number, pin_input) > 0:
            valid_account = True
            self.correct_pin = pin_input
            self.correct_number = account_number

        if valid_account:
            print("You have successfully logged in!")
            self.logged_menu()
        else:
            print("Wrong card number or PIN")
            self.main_menu()

    def logged_menu(self):
        options = {'1.': "Balance", '2.': "Add income", '3.': 'Do transfer',
                   '4.': 'Close account', '5.': "Log out", '0.': "Exit"}
        for item, value in options.items():
            print(item, value)

        choice = int(input())

        if choice == 1:
            self.balance_func()
        elif choice == 2:
            self.add_income()
        elif choice == 3:
            self.do_transfer()
        elif choice == 4:
            self.close_account()
        elif choice == 5:
            self.log_out()
        elif choice == 0:
            self.exit_func()

    def balance_func(self):
        print("Balance: ", user_dataDB.balance(connection, self.correct_number))
        self.logged_menu()

    def add_income(self):
        added_income = int(input('Enter income: '))
        balance = user_dataDB.balance(connection, self.correct_number)
        new_balance = balance + added_income

        user_dataDB.update_balance(connection, new_balance, self.correct_number, self.correct_pin)
        print('Income was added')

        self.logged_menu()

    def do_transfer(self):
        print('Transfer')
        receiver = input('Enter card number: \n')

        # check if number passes the Luhn algorithm
        receiver_list = [int(n) for n in receiver]
        checksum_to_check = receiver_list[-1]

        if self.luhn_algorithm(receiver_list) != checksum_to_check:
            print('Probably you made a mistake in the card number. Please try again!')
        elif user_dataDB.account_check(connection, receiver) < 1:
            print('Such a card does not exist.')
        # check if passed number is in database
        elif receiver == self.correct_number:
            print("You can't transfer money to the same account!")
        else:
            money_to_withdraw = int(input('Enter how much money you want to transfer: '))
            sender_balance = user_dataDB.balance(connection, self.correct_number)
            if sender_balance < money_to_withdraw:
                print('Not enough money!')
            else:
                # adding money to receivers account and taking it from sender
                receiver_balance = user_dataDB.balance(connection, receiver)
                updated_balance_s = sender_balance - money_to_withdraw
                updated_balance_r = receiver_balance + money_to_withdraw

                user_dataDB.transfer_money(connection, updated_balance_r, receiver)
                user_dataDB.transfer_money(connection, updated_balance_s, self.correct_number)

        self.logged_menu()

    def close_account(self):
        user_dataDB.delete_account(connection, self.correct_number, self.correct_pin)
        print('The account has been closed!')
        self.main_menu()

    def log_out(self):
        print("You have successfully logged out!")
        self.main_menu()

    @staticmethod
    def exit_func():
        print("Bye!")


new_client = Bank()
new_client.main_menu()
