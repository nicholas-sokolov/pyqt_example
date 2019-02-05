import sqlite3


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


@singleton
class Sql:

    def __init__(self, filename):
        self.connect = sqlite3.connect(filename)
        self.cursor = None

    def __del__(self):
        self._commit()

    def create_insert(self, query):
        self.cursor = self.connect.cursor()
        self.cursor.execute(query)
        self.connect.commit()

    def select(self, query):
        self.cursor = self.connect.cursor()
        self.cursor.execute(query)
        headers = [item[0] for item in self.cursor.description]
        return headers, self.cursor.fetchall()

