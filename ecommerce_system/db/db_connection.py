import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Create a database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False

    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")

    def execute_query(self, query, params=None):
        """Execute a query that doesn't return data (INSERT, UPDATE, DELETE)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return False

    def fetch_all(self, query, params=None):
        """Execute a SELECT query and return all results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Execute a SELECT query and return one result"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None


# Global database instance
db = DatabaseConnection()