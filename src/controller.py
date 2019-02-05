import os
import sqlite3

from PyQt5 import QtCore

from src.signals import signals
from src.worker import Worker


class Controller:

    def __init__(self):
        self.connect = None
        self.cursor = None
        self.query = None
        self.thread_pool = QtCore.QThreadPool()
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
        if not os.path.exists(database):
            signals.error_received.emit(f"No such file '{database}'")
            return
        # try connect
        try:
            self.connect = sqlite3.connect(database, isolation_level=None,
                                           check_same_thread=False)
            self.cursor = self.connect.cursor()
            signals.show_status.emit(f'Connect to {database}')
            signals.change_connect_button.emit()
        except Exception as err:
            signals.error_received.emit(f'{err}')

    def sql_listener(self, query):
        """
        :param str query:
        """
        self.query = query.strip()
        signals.show_status.emit(f'Processing.... {self.query}')
        try:
            response = self.cursor.execute(self.query)
            worker = Worker(response.fetchall)
            worker.signals.result.connect(self.received_sql_data)
            worker.signals.finished.connect(self.request_done)
            self.thread_pool.start(worker)
        except Exception as err:
            signals.error_received.emit(f'Error: {err}')
            self.request_done()

    def request_done(self):
        signals.show_status.emit(f'Done: {self.query}')

    def received_sql_data(self, data):
        if data:
            headers = [item[0] for item in self.cursor.description]
            signals.draw_table.emit(headers, data)
