import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager


class MySQLDatabase:
    def __init__(self, config):
        self.host = config['host']
        self.database = config['database']
        self.user = config['user']
        self.password = config['password']
        self.connection = None

    @contextmanager
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            yield self.connection
        except Error as e:
            print(f"Error: {e}")
            yield None
        finally:
            if self.connection and self.connection.is_connected():
                self.connection.close()

    def fetch_logs(self):
        try:
            with self.connect() as connection:
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM viewlogs")
                    rows = cursor.fetchall()
                    return rows
                else:
                    return []
        except Error as e:
            print(f"Error fetching logs: {e}")
            return []
