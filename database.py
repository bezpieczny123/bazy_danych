import mysql.connector

DB_NAME = 'expenses_db'
password = '1234'


def init_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password
    )
    cursor = connection.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
    connection.close()

   
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database=DB_NAME
    )
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(255),
            cost DECIMAL(10, 2),
            place VARCHAR(255)
        )
    ''')
    connection.commit()
    connection.close()



def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database=DB_NAME
    )


def insert_expense(name, category, cost, place):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (name, category, cost, place) VALUES (%s, %s, %s, %s)',
        (name, category, cost, place)
    )
    conn.commit()
    conn.close()


def get_all_expenses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * from expenses ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows