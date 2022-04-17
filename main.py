from sys import argv, exit

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from numpy import ndarray

from Entity.Game import Game
from Thread.RepeatedTask import RepeatedTimer
from Thread.VideoThread import VideoThread
from Utils import Constants
from Utils.Utility import convert_cv_qt


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(Constants.WINDOW_TITLE)
        self.image_label = QLabel(self)
        self.image_label.resize(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)

        self.game = Game(Constants.BLOCKS_BOARD_SIZE)
        self.game.draw_game_structure()

        self.can_detect_hand = False
        self.is_inverted = False

        RepeatedTimer(Constants.HAND_DETECTION_RATE, self.invert_can_detect_hand)
        RepeatedTimer(Constants.INVERSION_RATE, self.invert_is_inverted)

        self.thread = VideoThread(Constants.VIDEO_STREAM_ADDRESS)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, frame: ndarray):
        if self.can_detect_hand:
            self.game.detect_gesture(frame)
            if self.game.player.is_visible:
                self.game.clear_last_surface()
                self.game.draw_surface()

        self.game.move_ball()
        self.game.blend(frame)
        self.draw_status_text()
        self.set_frame_within_label(~frame if self.is_inverted else frame)

    def draw_status_text(self):
        cv2.putText(self.game.get_drawer_output(), "Game Status: " +
                    ("Playing" if self.game.game_status is None else (
                        "You win" if self.game.game_status else "You lose")),
                    (int(Constants.SCREEN_WIDTH / 2) - 80, Constants.SCREEN_HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255) if self.game.game_status else (255, 100, 40), thickness=2)

    def invert_can_detect_hand(self):
        self.can_detect_hand = not self.can_detect_hand

    def invert_is_inverted(self):
        self.is_inverted = not self.is_inverted

    def set_frame_within_label(self, frame: ndarray):
        qt_img = convert_cv_qt(frame)
        self.image_label.setPixmap(qt_img)


if __name__ == "__main__":
    q_app = QApplication(argv)
    app = App()
    app.show()
    exit(q_app.exec_())
