import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.pyqtSignal()


class TranslucentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TranslucentWidget, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.fillColor = QtGui.QColor(30, 30, 30, 120)
        # self.penColor = QtGui.QColor("#333333")

        # self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        # self.popup_penColor = QtGui.QColor(200, 200, 200, 255)

        self.close_btn = QtWidgets.QPushButton(self)
        self.close_btn.setText("CLICK ME")
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("background-color: rgb(0, 0, 0, 0)")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self._onclose)

        self.SIGNALS = TranslucentWidgetSignals()

    def resizeEvent(self, event):
        # s = self.size()
        # popup_width = 300
        # popup_height = 120
        # ow = int(s.width() / 2 - popup_width / 2)
        # oh = int(s.height() / 2 - popup_height / 2)
        self.close_btn.move(333, 444)

    def paintEvent(self, event):
        # This method is, in practice, drawing the contents of
        # your window.

        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, s.width(), s.height())
        qp.end()

    def _onclose(self):
        print("Close")
        self.SIGNALS.CLOSE.emit()


class ParentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ParentWidget, self).__init__(parent)

        # self._popframe = TranslucentWidget(self)
        # self._popframe.move(0, 0)
        # self._popframe.resize(self.width(), self.height())
        # self._popframe.SIGNALS.CLOSE.connect(self._closepopup)
        # self._popflag = True
        # self._popframe.show()

        self._popframe = None
        self._popflag = False

    def resizeEvent(self, event):
        if self._popflag:
            self._popframe.move(0, 0)
            self._popframe.resize(self.width(), self.height())

    def _onpopup(self):
        self._popframe = TranslucentWidget(self)
        self._popframe.move(0, 0)
        self._popframe.resize(self.width(), self.height())
        self._popframe.SIGNALS.CLOSE.connect(self._closepopup)
        self._popflag = True
        self._popframe.show()

    def _closepopup(self):
        self._popframe.close()
        self._popflag = False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = ParentWidget()
    main.resize(500, 500)
    main.show()
    sys.exit(app.exec_())
