import sqlite3

from src.signals import signals


class Controller:

    def __init__(self):
        self.connect = None
        self.cursor = None
        self.connect_signals()

    def disconnect(self):
        if self.connect:
            self.connect.close()
        self.connect = None
        self.cursor = None

    def connect_signals(self):
        signals.sql_sender.connect(self.sql_listener)
        signals.connect_button.connect(self.connect_process)

    def connect_process(self, database):
        if not database:
            signals.show_status.emit(f'Input path to database. Please')
            return
        if self.connect:
            self.disconnect()
            signals.show_status.emit(f'Close connect with {database}')
            signals.change_connect_button.emit()
            return
        # try connect
        try:
            self.connect = sqlite3.connect(database, isolation_level=None)
            self.cursor = self.connect.cursor()
            signals.show_status.emit(f'Connect to {database}')
            signals.change_connect_button.emit()
        except Exception as err:
            signals.error_received.emit(f'{err}')

    def sql_listener(self, query):
        """
        :param str query:
        """
        try:
            response = self.cursor.execute(query)
            signals.show_status.emit(f'Done: {query}')
            results = response.fetchall()

            if results:
                headers = [item[0] for item in self.cursor.description]
                signals.draw_table.emit(headers, results)
        except Exception as err:
            signals.error_received.emit(f'Invalid query to DB: {err}')
