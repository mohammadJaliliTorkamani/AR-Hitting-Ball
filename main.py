import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout

from Entity.Game import Game
from Thread.VideoThread import VideoThread
from Utils.Drawer import Drawer
from Utils.Utility import convert_cv_qt

class App(QWidget):

    def __init__(self, display_width, display_height, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.display_width = display_width
        self.display_height = display_height
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)

        self.drawer = Drawer()
        self.game = Game((4, 9), (self.display_width, self.display_height), self.drawer)
        self.game.draw_game_structure()

        self.interrupt_to_detect_hand_counter = 0
        self.structure_is_created = False

        self.thread = VideoThread("https://192.168.1.155:8080/video", self.display_width, self.display_height)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        self.interrupt_to_detect_hand_counter = (self.interrupt_to_detect_hand_counter + 1) % 3
        if self.interrupt_to_detect_hand_counter == 0:
            self.game.detect_gesture(cv_img)
            if self.game.player.is_visible:
                self.game.clear_last_surface()
                self.game.draw_surface()

        self.game.move_ball()
        self.show_cv_img_in_frame(cv_img)

    def show_cv_img_in_frame(self, cv_img):
        self.drawer.blend(cv_img)
        qt_img = convert_cv_qt(self.drawer.output, self.display_width, self.display_height)
        self.image_label.setPixmap(qt_img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App(1280, 960, "Tik Tak Toe")
    a.show()
    sys.exit(app.exec_())
