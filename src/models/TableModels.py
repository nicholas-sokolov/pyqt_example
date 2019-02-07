from PyQt5 import QtCore


class SqlResultTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.header = []
        self.datatable = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.datatable)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.header)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        elif Qt_Orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.header[p_int])
        elif Qt_Orientation == QtCore.Qt.Vertical:
            return QtCore.QVariant(p_int + 1)
        return QtCore.QVariant()

    def add_results(self, chunk):
        self.beginResetModel()
        self.datatable += chunk
        self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self.datatable = []
        self.header = []
        self.endResetModel()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            if self.datatable:
                return self.datatable[index.row()][index.column()]
            else:
                return QtCore.QVariant()
        return QtCore.QVariant()
