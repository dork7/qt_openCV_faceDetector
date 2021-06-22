import sys
from os import path

import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

import inspect
from PyQt5 import Qt
# from overlayButton import TranslucentWidget
from sigs import WidgetSignals
import os


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)

        # self.camera = Piself.camera()
        # self.camera.framerate = 35
        # self.camera.rotation = 90
        # self.camera.hflip=True
        # self.camera.resolution = (480, 640)
        # # raw_capt = PiRGBArray(camera, size=(480, 640))

        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        vers = ['%s = %s' % (k, v) for k, v in vars(Qt).items() if k.lower().find(
            'version') >= 0 and not inspect.isbuiltin(v)]
        print('\n'.join(sorted(vers)))
        # self.timer.start(0, self)

    def start_recording(self):
        print("Clikd")
        self.timer.start(0, self)

    def stop_recording(self):
        self.timer.stop()

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        maskNet = load_model("mask_detector.model")
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._green = (0, 255, 0)
        self._width = 2
        self._min_size = (30, 30)
        self.displayWidth = 480
        self.displayHeight = 640

        # button shit

        self.close_btn = QtWidgets.QPushButton(self)
        # self.close_btn.setText("CLICK ME")
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setFixedSize(30, 30)

        self.close_btn.setIcon(QtGui.QIcon('btn_icon.png'))
        self.close_btn.setIconSize(QtCore.QSize(40, 30))
        self.close_btn.setStyleSheet('QPushButton{border: 0px solid;}')
        #     "background-image: url('btn_icon.png'); border: none;")
        self.close_btn.move(380, 320)
        self.close_btn.clicked.connect(self._onclose)

        self.SIGNALS = WidgetSignals()

    def _onclose(self):
        print("Close")
        self.SIGNALS.CLOSE.emit()

    def detect_faces(self, frame):
        # frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25,
        #                    interpolation=cv2.INTER_AREA)
        (h, w) = frame.shape[:2]
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        det_faces = self.classifier.detectMultiScale(gray_image,
                                                     scaleFactor=1.3,
                                                     minNeighbors=4,
                                                     flags=cv2.CASCADE_SCALE_IMAGE,
                                                     minSize=self._min_size)
        # print(faces)
        # return faces
        faces = []
        faces_tf = []
        locs = []
        preds = [[0, 0]]

        print(det_faces)
        for (x, y, w, h) in det_faces:

            startX = x
            startY = y
            endX = w
            endY = h
            locs.append((startX, startY, endX, endY))
            face = frame[startY:startY + endY, startX:startX+endX]
            faces.append(face)
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            faces_tf.append(face)

        return locs, det_faces, faces_tf

    def image_data_slot(self, image_data):
        locs, faces, faces_tf = self.detect_faces(image_data)
        for (x, y, w, h) in faces:
            cv2.rectangle(image_data,
                          (x, y),
                          (x+w, y+h),
                          self._green,
                          self._width)
            # preds_tf = self.detect_mask(faces_tf, self.maskNet)
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            print(self.image.size())
            self.setFixedSize(self.image.size())

        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(image)
        pixmap4 = pixmap.scaled(
            self.displayHeight, self.displayWidth, QtCore.Qt.KeepAspectRatio)
        image = pixmap4.toImage()
        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        # s = self.size()
        painter = QtGui.QPainter(self)
        # painter = QtGui.painterainter()
        # painter.begin(self)
        # painter.setRenderHint(QtGui.painterainter.Antialiasing, True)
        # painter.setPen(self.penColor)
        # painter.setBrush(self.fillColor)
        # painter.drawRect(0, 0, s.width(), s.height())

        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def detect_mask(faces, maskNet):
        preds = None
        if len(faces) > 0:
            faces = np.array(faces, dtype="float32")
            preds = maskNet.predict(faces, batch_size=1)[0]
        return preds

    def _onclose(self):
        print("Close")
        self.SIGNALS.CLOSE.emit()
