import mysql.connector
from secret import HOST, USER, PASSWD
from config import CATEGORIES

class Database:
    """This class is used for every iteraction with the database,
    even creating it if it doesn't exist yet"""

    def __init__(self):
        """create the connector and create the database and 
        all required elements if they don't exist yet
        """
        self.connector = mysql.connector.connect(
        host = HOST,
        user = USER,
        passwd = PASSWD
        )
        self.mycursor = self.connector.cursor()
        self.create_database()
        self.create_table_categories()
        self.insert_categories()

    def create_database(self):
        """Create the database if it doesn't exis then update the connector"""
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS OpenFF")

        self.connector = mysql.connector.connect(
        host = HOST,
        user = USER,
        passwd = PASSWD,
        database = 'OpenFF'
        )
        self.mycursor = self.connector.cursor()

    def create_table_categories(self):
        """Create the table Categories"""
        table = "CREATE TABLE IF NOT EXISTS Categories" +\
                "(id INTEGER(2) PRIMARY KEY NOT NULL AUTO_INCREMENT," +\
                "name VARCHAR(155) NOT NULL)"
        self.mycursor.execute(table)

    def insert_categories(self):
        """Insert the categories into their table"""
        cat_query = self.get_categories()
        if cat_query == None:
            query = "INSERT INTO Categories (name) VALUES (%s)"
            self.mycursor.executemany(query, CATEGORIES)
            self.connector.commit()

    def get_categories(self):
        """Return all the categories"""
        self.mycursor.execute("SELECT * FROM Categories")
        result = self.mycursor.fetchall()
        return result

    def create_table_alternative(self):
        """create the table of alternative product
        if it doesn't exist
        """
        query = "CREATE TABLE IF NOT EXISTS Alternative" +\
                "(id INTERGER(2) PRIMARY KEY NOT NUL AUTO_INCREMENT," +\
                "name VARCHAR (155) NOT NULL," +\
                "product_ID INTEGER (2) NOT NULL)"
        self.mycursor.execute(query)

    def insert_alternative(self, product):
        """Add the substitute product to the database"""
        query = "INSERT INTO Alternative (name, product_ID) VALUES (%s, %s)"
        self.mycursor.execute(query)

    def create_table_product(self):
        """Create the table of product if it doesn't exist"""
        query = "CREATE TABLE IF NOT EXISTS Product" +\
                "(id INTERGER(2) PRIMARY KEY NOT NUL AUTO_INCREMENT," +\
                "name VARCHAR (155) NOT NULL," +\
                "category_ID INTEGER (2) NOT NULL)"
        self.mycursor.execute(query)