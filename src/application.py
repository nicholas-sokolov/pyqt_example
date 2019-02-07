from PyQt5 import QtWidgets

from src.controller import Controller
from src.signals import signals
from src.view.main_widget import MainWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = Controller()
        self.error_msg = QtWidgets.QErrorMessage(self)
        self.yes_no_msg = QtWidgets.QMessageBox(self)

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        self.setup_ui()
        self.connect_signals()

    def connect_signals(self):
        signals.error_received.connect(self.show_error)
        signals.show_status.connect(self.statusBar().showMessage)
        signals.show_yes_no_dialog.connect(self.show_dialog)

    def show_dialog(self, message, query):
        ret = self.yes_no_msg.question(self, '', message,
                                       self.yes_no_msg.Yes |
                                       self.yes_no_msg.No)
        if ret == self.yes_no_msg.Yes:
            signals.sql_sender.emit(query, False)

    def show_error(self, error_msg):
        self.error_msg.showMessage(error_msg)

    def setup_ui(self):
        self.setWindowTitle("PyQt Example")
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        width = screen.width() / 3
        height = screen.height() / 3
        self.setMinimumSize(width, height)
        self.move(width, height)
