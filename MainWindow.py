from PyQt5.sip import delete
from sigs import WidgetSignals
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from types import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from appUI import Ui_MainWindow
from detectorWidget import FaceDetectionWidget, RecordVideo
from sigs import WidgetSignals
import sys


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.main_win.setMaximumSize(480, 640)
        self.main_win.setMinimumSize(480, 640)
        self.main_win.setAttribute(Qt.WA_AcceptTouchEvents)
        self.redImg = QPixmap('images/redImg.jpg')
        self.blueImg = QPixmap('images/blueImg.jpg')

        fp = 'haarcascade_frontalface_default.xml'
        self.ui.stackedWidget.setCurrentIndex(0)
        self.face_detection_widget = FaceDetectionWidget(fp)

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QVBoxLayout()
        layout.addWidget(self.face_detection_widget)

        self.ui.widget.setLayout(layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.time)
        self.timer.start(0000)
        self.timer.isSingleShot()
        self.SIGNALS = WidgetSignals()
        self.face_detection_widget.SIGNALS.CLOSE.connect(self.showTempPg)
        self.ui.pushButton_2.clicked.connect(self.showSettings)
        self.ui.pushButton_3.clicked.connect(self.time)

    def time(self):
        # self.label.hide()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.record_video.start_recording()
        self.timer.stop()

    def show(self):
        self.main_win.show()

    def showTempPg(self):
        print("camera close called")
        print("called")
        self.record_video.stop_recording()
        # change index to 3 to see setting page
        self.ui.stackedWidget.setCurrentIndex(3)
        # set image on the basis of detector
        detected = 1
        if detected:
            self.setTempImg(self.redImg)
        elif not detected:
            self.setTempImg(self.blueImg)

    def closeCamera(self):
        self.record_video.stop_recording()
        self.ui.stackedWidget.setCurrentIndex(3)

    def showSettings(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def setTempImg(self, img):
        self.ui.tempImg.setPixmap(img)
        self.ui.tempImg.show()
        self.timer.start(4000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
