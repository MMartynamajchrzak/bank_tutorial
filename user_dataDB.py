import sqlite3

CREATE_CARD_TABLE = """CREATE TABLE IF NOT EXISTS card (
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

BALANCE = "SELECT balance FROM card;"


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


def check_data(connection, number, pin):
    with connection:
        return connection.execute(CHECK_DATA, (number, pin)).fetchone()[0]


def balance(connection):
    with connection:
        return connection.execute(BALANCE).fetchone()[0]
