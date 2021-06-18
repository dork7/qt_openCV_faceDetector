from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from appUI import Ui_MainWindow
from detectorWidget import FaceDetectionWidget, RecordVideo
from overlayButton import TranslucentWidget
import sys


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        fp = 'haarcascade_frontalface_default.xml'
        self.ui.stackedWidget.setCurrentIndex(0)
        # self.ui.pushButton.clicked.connect(self.showTempPg)
        self.face_detection_widget = FaceDetectionWidget(fp)

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QVBoxLayout()
        layout.addWidget(self.face_detection_widget)

        # self.record_video.start_recording()

        self.ui.widget.setLayout(layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.time)
        self.timer.start(2000)
        self.timer.isSingleShot()
        # self.setLayout(layout)

    def time(self):
        # self.label.hide()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.record_video.start_recording()
        self.timer.stop()

    def show(self):
        self.main_win.show()

    def showTempPg(self):
        print("called")
        self.ui.stackedWidget.setCurrentIndex(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
