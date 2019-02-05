from PyQt5 import QtCore


class Signals(QtCore.QObject):
    show_status = QtCore.pyqtSignal(str)

    connect_button = QtCore.pyqtSignal(str)
    change_connect_button = QtCore.pyqtSignal()
    close_connection = QtCore.pyqtSignal()
    sql_sender = QtCore.pyqtSignal(str)

    error_received = QtCore.pyqtSignal(str)

    draw_table = QtCore.pyqtSignal(list, list)

    result = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal()


signals = Signals()
