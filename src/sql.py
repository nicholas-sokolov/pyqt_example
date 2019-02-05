import sqlite3


class Sql:

    def __init__(self, filename):
        self.connect = sqlite3.connect(filename)
        self.cursor = None

    def create_insert(self, query):
        self.cursor = self.connect.cursor()
        self.cursor.execute(query)
        self.connect.commit()

    def select(self, query):
        self.cursor = self.connect.cursor()
        self.cursor.execute(query)
        headers = [item[0] for item in self.cursor.description]
        return headers, self.cursor.fetchall()
