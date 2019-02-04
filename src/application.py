from PyQt5 import QtCore, QtGui, QtWidgets

from src.models.TableModels import SqlResultTableModel
from src.controller import Controller
from src.signals import signals


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = Controller()
        self.error_msg = QtWidgets.QErrorMessage(self)

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        self.setup_ui()
        self.connect_signals()

    def connect_signals(self):
        signals.error_received.connect(self.show_error)

    def show_error(self, error_msg):
        self.error_msg.showMessage(error_msg)

    def setup_ui(self):
        self.setWindowTitle("PyQt Example")
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        width = screen.width() / 3
        height = screen.height() / 3
        self.setMinimumSize(width, height)
        self.move(width, height)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.sql_connection = QtWidgets.QLineEdit()
        self.sql_connection.setText(':memory:')
        self.query_field = QtWidgets.QLineEdit()

        form = QtWidgets.QFormLayout()
        form.addRow('Sql connection', self.sql_connection)
        form.addRow('Query to DB', self.query_field)

        self.button = QtWidgets.QPushButton("Send")
        self.button.setFixedWidth(200)
        self.button.clicked.connect(self.make_query)

        self.table = QtWidgets.QTableView(self)
        self.table_model = SqlResultTableModel(self)
        self.table.setModel(self.table_model)

        self.layout.addLayout(form)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.connect_signals()

    def connect_signals(self):
        signals.draw_table.connect(self.fill_data_table)

    def fill_data_table(self, header, data):
        """ Fill header and cells

        :param list header: Columns
        :param list data: Received data
        """
        if not data:
            signals.error_received.emit('No data to show')
        self.table_model.header = header
        self.table_model.insertRows(data)

    def make_query(self):
        query = self.query_field.text()
        if not query:
            signals.error_received.emit('No query')
            return
        connection_name = self.sql_connection.text()
        signals.make_query.emit(connection_name, query)

    def clear_widgets(self):
        self.query_field.clear()


