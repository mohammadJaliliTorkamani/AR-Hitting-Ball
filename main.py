import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout

from Thread.VideoThread import VideoThread
from Utils.Utility import convert_cv_qt


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tik-Tak-Toe Game!")
        self.display_width = 1280
        self.display_height = 960
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)
        self.structure_is_created = False

        self.thread = VideoThread("https://192.168.1.155:8080/video", self.display_width, self.display_height)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        self.show_cv_img_in_frame(cv_img)

    def show_cv_img_in_frame(self, cv_img):
        qt_img = convert_cv_qt(cv_img, self.display_width, self.display_height)
        self.image_label.setPixmap(qt_img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
