from PyQt5 import QtCore


class Signals(QtCore.QObject):

    make_query = QtCore.pyqtSignal(str, str)

    error_received = QtCore.pyqtSignal(str)

    draw_table = QtCore.pyqtSignal(list, list)


signals = Signals()
