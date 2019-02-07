from PyQt5 import QtCore


class Signals(QtCore.QObject):
    # Service
    show_status = QtCore.pyqtSignal(str)
    error_received = QtCore.pyqtSignal(str)
    connect_button = QtCore.pyqtSignal(str)
    change_connect_button = QtCore.pyqtSignal()

    # DB signals
    sql_sender = QtCore.pyqtSignal(str, bool)
    db_rows_received = QtCore.pyqtSignal(list)
    headers_received = QtCore.pyqtSignal(list)
    sql_query_done = QtCore.pyqtSignal()

    show_yes_no_dialog = QtCore.pyqtSignal(str, str)


signals = Signals()
