import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from numpy import ndarray

from Thread.RepeatedTask import RepeatedTimer
from Utils import Constants


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, camera_port: str, display_width: int = Constants.SCREEN_WIDTH,
                 display_height: int = Constants.SCREEN_HEIGHT):
        super(VideoThread, self).__init__()
        self.port = camera_port
        self.inverted = False
        self.display_width = display_width
        self.display_height = display_height

    def run(self):
        cap = cv2.VideoCapture(self.port)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_width)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_height)

        RepeatedTimer(Constants.INVERSION_RATE, self.invert_is_inverted)

        while True:
            ret, frame = cap.read()
            if ret:
                if frame is not None:
                    frame = ~cv2.flip(frame, 1) if self.inverted else cv2.flip(frame, 1)
                    self.change_pixmap_signal.emit(frame)

    def invert_is_inverted(self):
        self.inverted = not self.inverted
