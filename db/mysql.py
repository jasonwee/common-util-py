import mysql.connector

# pip install mysql-connector-python
# https://www.w3schools.com/python/python_mysql_getstarted.asp
class Mysql:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.username,
            password = self.password
        )

    # create
    def create(self, statement, vals=()):
        # create database mydb
        # show databases
        # CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))
        #"INSERT INTO customers (name, address) VALUES (%s, %s)" | ("John", "Highway 21")
        # "DROP TABLE customers"
        # "DROP TABLE IF EXISTS customers"
        cursor = self.mydb.cursor()
        if vals:
            cursor.execute(statement, vals)
            self.mydb.commit()
            return cursor.rowcount
        else:
            cursor.execute(statement)

    # read
    def read(self, statement, vals=()):
        # SELECT * FROM customers
        # SELECT name, address FROM customers
        # SELECT * FROM customers WHERE address ='Park Lane 38'
        # SELECT * FROM customers WHERE address = %s | ("Yellow Garden 2", )
        # SELECT * FROM customers ORDER BY name
        # SELECT * FROM customers ORDER BY name DESC
        # SELECT * FROM customers LIMIT 5
        # SELECT * FROM customers LIMIT 5 OFFSET 2
        # "SELECT users.name AS user, products.name AS favorite FROM users INNER JOIN products ON users.fav = products.id
        cursor = self.mydb.cursor()
        if vals:
            cursor.execute(statement, vals)
        else:
            cursor.execute(statement)
        results = cursor.fetchall()
        return results

    # update
    def update(self, statement, vals=()):
        # "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
        # "UPDATE customers SET address = %s WHERE address = %s" | ("Valley 345", "Canyon 123")
        cursor = self.mydb.cursor()
        if vals:
            cursor.execute(statement, val)
        else:
            cursor.execute(statement)
        self.mydb.commit()
        return cursor.rowcount

    # delete
    def delete(self, statement, vals=()):
        # DELETE FROM customers WHERE address = 'Mountain 21'
        # DELETE FROM customers WHERE address = %s | ("Yellow Garden 2", )
        cursor = self.mydb.cursor()
        if vals:
            cursor.execute(statement, vals)
        else:
            cursor.execute(statement)
        self.mydb.commit()
        return cursor.rowcount

    # general method, just return cursor, let caller do it.
    def get_cursor(self):
        return self.mydb.cursor()
