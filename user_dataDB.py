import sqlite3

CREATE_CARD_TABLE = """CREATE TABLE IF NOT EXISTS card1 (
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
        );"""

INSERT_CARD = """
        INSERT INTO card (number, pin, balance) 
        VALUES (?,?,0)
        ;
        """

CHECK_DATA = "SELECT COUNT(*) FROM card WHERE number = ? AND pin = ? ;"

BALANCE = "SELECT balance FROM card WHERE number = ?;"

UPDATED_BALANCE = "UPDATE card SET balance = ? WHERE number = ? AND pin = ?"

CLOSE_ACCOUNT = "DELETE FROM card WHERE number = ? AND pin = ?"

ACCOUNT_NUM = "SELECT COUNT(*) FROM card WHERE number = ?;"

SEND_TO_OTHER_ACCOUNT = "UPDATE card SET balance = ? WHERE number = ?"


def connect():
    return sqlite3.connect('card.s3db')


def create_table(connection):
    with connection:
        connection.execute(CREATE_CARD_TABLE)
        connection.commit()


def save_data(connection, number, pin):
    with connection:
        connection.execute(INSERT_CARD, (number, pin))
        connection.commit()


def update_balance(connection, new_balance, number, pin):
    with connection:
        connection.execute(UPDATED_BALANCE, (new_balance, number, pin))
        connection.commit()


def transfer_money(connection, new_balance, number):
    with connection:
        connection.execute(SEND_TO_OTHER_ACCOUNT, (new_balance, number))
        connection.commit()


def check_data(connection, number, pin):
    with connection:
        return connection.execute(CHECK_DATA, (number, pin)).fetchone()[0]


def balance(connection, number):
    with connection:
        return connection.execute(BALANCE, (number,)).fetchone()[0]


def delete_account(connection, number, pin):
    with connection:
        connection.execute(CLOSE_ACCOUNT, (number, pin))
        connection.commit()


def account_check(connection, number):
    with connection:
        return connection.execute(ACCOUNT_NUM, (number,)).fetchone()[0]

