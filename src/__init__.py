import sys
import traceback

from PyQt5 import QtWidgets

from src.application import MainWindow


def run_app():
    qapp = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()

    def exception_hook(*args):
        print(''.join(traceback.format_exception(*args)))

    sys.excepthook = exception_hook

    sys.exit(qapp.exec_())
