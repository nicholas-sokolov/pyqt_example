import sys
import traceback

from PyQt5 import QtCore


class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.

                    Supported signals are:
    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    progress
        `int` indicating % progress

    """
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int)


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
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(self.result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
