import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from Utils import Constants


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, camera_port: str, display_width: int = Constants.SCREEN_WIDTH,
                 display_height: int = Constants.SCREEN_HEIGHT):
        super(VideoThread, self).__init__()
        self.port = camera_port
        self.display_width = display_width
        self.display_height = display_height

    def run(self):
        cap = cv2.VideoCapture(self.port)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_height)

        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                if frame is not None:
                    self.change_pixmap_signal.emit(frame)
