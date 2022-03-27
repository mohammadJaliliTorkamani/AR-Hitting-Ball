import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    hand_detection_signal = pyqtSignal(np.ndarray)

    def __init__(self, camera_port, display_width, display_height):
        super(VideoThread, self).__init__()
        self.port = camera_port
        self.display_width = display_width
        self.display_height = display_height

    def run(self):
        cap = cv2.VideoCapture(self.port)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_height)

        while True:
            ret, cv_img = cap.read()
            if ret:
                cv_img = cv2.flip(cv_img, 1)
                self.change_pixmap_signal.emit(cv_img)