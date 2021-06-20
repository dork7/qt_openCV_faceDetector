import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class WidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.pyqtSignal()
