from PyQt5 import QtWidgets

from src.models.TableModels import SqlResultTableModel
from src.signals import signals

CONNECT = 'connect'
DISCONNECT = 'disconnect'


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_connect = False

        connection = QtWidgets.QLabel('Sql connection:')
        self.connection_field = QtWidgets.QLineEdit()
        self.connection_field.setText(':memory:')
        self.connection_button = QtWidgets.QPushButton(CONNECT)

        query = QtWidgets.QLabel('Query to DB:')
        self.query_field = QtWidgets.QLineEdit()
        self.query_button = QtWidgets.QPushButton("Send")
        self.query_button.setFixedWidth(200)

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
        self.connection_button.clicked.connect(self.connect_to_db)
        self.query_button.clicked.connect(self.make_query)
        signals.draw_table.connect(self.fill_data_table)
        signals.connection_button_trigger.connect(self.check_connection)

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
        signals.set_connection.emit(database)

    def check_connection(self):
        if not self.is_connect:
            self.is_connect = True
            self.connection_button.setText(DISCONNECT)
        else:
            self.is_connect = False
            self.connection_button.setText(CONNECT)
        self.connection_field.setDisabled(self.is_connect)

    def make_query(self):
        query = self.query_field.text()
        if not query:
            signals.error_received.emit('No query')
            return
        connection_name = self.connection_field.text()
        signals.make_query.emit(connection_name, query)

    def clear_widgets(self):
        self.query_field.clear()
