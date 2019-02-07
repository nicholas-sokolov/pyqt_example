from PyQt5 import QtCore

from src.signals import signals


class QueryThread(QtCore.QThread):

    def __init__(self, response, buffer_size=3000, parent=None):
        super().__init__(parent)
        self.response = response
        self.buffer_size = buffer_size

    def run(self):
        data_buffer = []
        if not self.response:
            return
        try:
            for item in self.response:
                data_buffer.append(list(item))
                if len(data_buffer) >= self.buffer_size:
                    signals.db_rows_received.emit(data_buffer)
                    data_buffer = []
            signals.db_rows_received.emit(data_buffer)
        except Exception as err:
            signals.error_received.emit(f'Error: {err}')
