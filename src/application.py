from PyQt5 import QtWidgets

from src.controller import Controller
from src.signals import signals
from src.view.main_widget import MainWidget


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
        signals.show_status.connect(self.statusBar().showMessage)

    def show_error(self, error_msg):
        self.error_msg.showMessage(error_msg)

    def setup_ui(self):
        self.setWindowTitle("PyQt Example")
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        width = screen.width() / 3
        height = screen.height() / 3
        self.setMinimumSize(width, height)
        self.move(width, height)
