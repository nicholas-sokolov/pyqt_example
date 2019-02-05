from PyQt5 import QtWidgets

from src.models.TableModels import SqlResultTableModel
from src.signals import signals

CONNECT = 'connect'
DISCONNECT = 'disconnect'


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        connection = QtWidgets.QLabel('Sql connection:')
        self.connection_field = QtWidgets.QLineEdit()
        self.connection_field.setText(':memory:')
        self.connection_button = QtWidgets.QPushButton(CONNECT)
        self.connection_button.setDisabled(False)

        query = QtWidgets.QLabel('Query to DB:')
        self.query_field = QtWidgets.QLineEdit()
        self.query_field.setDisabled(True)
        self.query_button = QtWidgets.QPushButton("Send")
        self.query_button.setDisabled(True)

        result = QtWidgets.QLabel('Result:')
        self.result_table = QtWidgets.QTableView(self)
        self.result_table_model = SqlResultTableModel(self)
        self.result_table.setModel(self.result_table_model)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(connection, 1, 0)
        grid.addWidget(self.connection_field, 1, 1)
        grid.addWidget(self.connection_button, 1, 2)

        grid.addWidget(query, 2, 0)
        grid.addWidget(self.query_field, 2, 1)
        grid.addWidget(self.query_button, 2, 2)

        grid.addWidget(result, 3, 0)
        grid.addWidget(self.result_table, 3, 1, 5, 2)

        self.setLayout(grid)
        self.connect_signals()

    def connect_signals(self):
        self.connection_field.textChanged.connect(self.check_connection_button)
        self.query_field.textChanged.connect(self.check_send_button)
        self.connection_button.clicked.connect(self.connect_to_db)
        self.query_button.clicked.connect(self.send_request)
        signals.draw_table.connect(self.fill_data_table)
        signals.change_connect_button.connect(self.check_connection)

    def check_connection_button(self):
        if not self.connection_field.text():
            self.connection_button.setDisabled(True)
        else:
            self.connection_button.setDisabled(False)

    def check_send_button(self):
        if not self.connection_field.text() or not self.query_field.text():
            self.query_button.setDisabled(True)
        else:
            self.query_button.setDisabled(False)

    def fill_data_table(self, header, data):
        """ Fill header and cells

        :param list header: Columns
        :param list data: Received data
        """
        if not data:
            signals.error_received.emit('No data to show')
        self.result_table_model.header = header
        self.result_table_model.insertRows(data)

    def connect_to_db(self):
        database = self.connection_field.text()
        signals.connect_button.emit(database)

    def check_connection(self):
        self.connection_field.setDisabled(self.connection_button.text() == CONNECT)
        self.query_field.setDisabled(self.connection_button.text() == DISCONNECT)
        if self.connection_button.text() == CONNECT:
            self.connection_button.setText(DISCONNECT)
            if self.query_field.text():
                self.query_button.setDisabled(False)
        else:
            self.query_button.setDisabled(True)
            self.connection_button.setText(CONNECT)

    def send_request(self):
        query = self.query_field.text()
        if not query:
            signals.error_received.emit('No query')
            return
        signals.sql_sender.emit(query)

    def clear_widgets(self):
        self.query_field.clear()
