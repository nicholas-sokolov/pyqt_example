import sqlite3


class Sql:

    def __init__(self, filename):
        self.filename = filename
        self.connect = None
        self.cursor = None

    def __del__(self):
        self._commit()

    def _connect(self):
        self.connect = sqlite3.connect(self.filename)
        self.cursor = self.connect.cursor()

    def _commit(self):
        self.connect.commit()
        self.connect.close()

    def create(self, query):
        self._connect()
        self.cursor.execute(query)
        self._commit()

    def insert(self, query):
        self._connect()
        self.cursor.execute(query)
        self._commit()

    def select(self, query):
        self._connect()
        self.cursor.execute(query)
        headers = [item[0] for item in self.cursor.description]
        return headers, self.cursor.fetchall()

