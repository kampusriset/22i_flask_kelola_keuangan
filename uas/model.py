import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_flask'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def create_user(username, password):
        db = Database()
        password_hash = generate_password_hash(password)
        db.cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                         (username, password_hash))
        db.connection.commit()
        db.close()

    @staticmethod
    def get_user_by_username(username):
        db = Database()
        db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db.cursor.fetchone()
        db.close()
        return user

    @staticmethod
    def verify_password(username, password):
        db = Database()
        db.cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = db.cursor.fetchone()
        db.close()
        if result:
            return check_password_hash(result[0], password)
        return False

    @staticmethod
    def update_password(username, new_password):
        db = Database()
        password_hash = generate_password_hash(new_password)
        db.cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s",
                         (password_hash, username))
        db.connection.commit()
        db.close()

class Transaction:
    def __init__(self, date, amount, description, type):
        self.date = date
        self.amount = amount
        self.description = description
        self.type = type

    @staticmethod
    def get_all_transactions(page=1, per_page=10, sort_by='date', sort_order='asc'):
        db = Database()
        offset = (page - 1) * per_page
        query = f"SELECT * FROM transactions ORDER BY {sort_by} {sort_order} LIMIT %s OFFSET %s"
        db.cursor.execute(query, (per_page, offset))
        transactions = db.cursor.fetchall()
        db.close()
        return transactions

    @staticmethod
    def get_transaction(id):
        db = Database()
        db.cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
        transaction = db.cursor.fetchone()
        db.close()
        return transaction

    @staticmethod
    def create_transaction(transaction):
        db = Database()
        db.cursor.execute("INSERT INTO transactions (date, amount, description, type) VALUES (%s, %s, %s, %s)",
        (transaction.date, transaction.amount, transaction.description, transaction.type))
        db.connection.commit()
        db.close()

    @staticmethod
    def update_transaction(id, transaction):
        db = Database()
        db.cursor.execute("UPDATE transactions SET date = %s, amount = %s, description = %s, type = %s WHERE id = %s",
        (transaction.date, transaction.amount, transaction.description, transaction.type, id))
        db.connection.commit()
        db.close()

    @staticmethod
    def delete_transaction(id):
        db = Database()
        db.cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
        db.connection.commit()
        db.close()

    @staticmethod
    def search_transactions(query):
        db = Database()
        db.cursor.execute("SELECT * FROM transactions WHERE description LIKE %s OR amount LIKE %s ", 
                          ('%' + query + '%', '%' + query + '%'))
        transactions = db.cursor.fetchall()
        db.close()
        return transactions

    @staticmethod
    def count_transactions():
        db = Database()
        db.cursor.execute("SELECT COUNT(*) FROM transactions")
        count = db.cursor.fetchone()[0]
        db.close()
        return count
