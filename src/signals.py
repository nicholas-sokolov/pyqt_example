from PyQt5 import QtCore


class Signals(QtCore.QObject):
    show_status = QtCore.pyqtSignal(str)

    set_connection = QtCore.pyqtSignal(str)
    connection_button_trigger = QtCore.pyqtSignal()
    close_connection = QtCore.pyqtSignal()
    make_query = QtCore.pyqtSignal(str, str)

    error_received = QtCore.pyqtSignal(str)

    draw_table = QtCore.pyqtSignal(list, list)


signals = Signals()
