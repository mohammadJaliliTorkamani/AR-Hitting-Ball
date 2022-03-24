import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout

from Entity.Game import Game
from Entity.Player import Player
from Thread.VideoThread import VideoThread
from Utils.Drawer import Drawer
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

        self.game = Game((4, 8), (self.display_width, self.display_height))
        self.drawer = Drawer()
        self.player = Player()

        self.interrupt_to_detect_open_hands_counter = 0

        self.thread = VideoThread("https://192.168.1.155:8080/video", self.display_width, self.display_height)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):

        if self.game.is_playing:
            self.player.detect_gesture()
            if self.player.visible and self.player.hand_status == 0:
                #handle_game_logic here

            elif self.player.visible and self.player.hand_status == 1:
                self.game.is_playing = False
        else:
            self.interrupt_to_detect_open_hands_counter = (self.interrupt_to_detect_open_hands_counter + 1) % 50
            if self.interrupt_to_detect_open_hands_counter == 0:
                self.player.detect_gesture()
                self.game.is_playing = True


        self.show_cv_img_in_frame(cv_img)

    def show_cv_img_in_frame(self, cv_img):
        self.drawer.blend(cv_img)
        qt_img = convert_cv_qt(self.drawer.output, self.display_width, self.display_height)
        self.image_label.setPixmap(qt_img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
