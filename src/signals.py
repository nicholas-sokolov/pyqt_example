from PyQt5 import QtCore


class Signals(QtCore.QObject):
    # Service
    show_status = QtCore.pyqtSignal(str)
    error_received = QtCore.pyqtSignal(str)
    connect_button = QtCore.pyqtSignal(str)
    change_connect_button = QtCore.pyqtSignal()

    # DB signals
    sql_sender = QtCore.pyqtSignal(str)
    db_rows_received = QtCore.pyqtSignal(list)
    headers_received = QtCore.pyqtSignal(list)
    sql_query_done = QtCore.pyqtSignal()


signals = Signals()
