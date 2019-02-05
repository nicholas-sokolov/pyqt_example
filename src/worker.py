import sqlite3

from PyQt5 import QtCore

from src.signals import signals


class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.

                    Supported signals are:
    finished
        No data
    result
        `object` data returned from processing, anything

    """
    finished = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    """
    Worker thread

    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    def __init__(self, func, *args, **kwargs):
        QtCore.QRunnable.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.result = None

    def run(self):
        """ Initialise the runner function with passed args, kwargs.

        :return:
        """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except sqlite3.OperationalError as err:
            signals.error_received.emit(err)
        except MemoryError:
            signals.error_received.emit('Memory error')
        else:
            # Return the result of the processing
            self.signals.result.emit(self.result)
        finally:
            self.signals.finished.emit()  # Done
