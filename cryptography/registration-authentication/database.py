import sqlite3


def create_table():
    cursor.execute("""CREATE TABLE users (login text, password text)""")


def fill_data():
    data = [('EAEgorov', '12344321'),
            ('admin', 'admin')]

    # Fill the data
    cursor.executemany("INSERT INTO users VALUES (?, ?)", data)
    connection.commit()


if __name__ == '__main__':
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    create_table()
    fill_data()
    query = "SELECT * FROM users"
    cursor.execute(query)
    print(cursor.fetchall())






