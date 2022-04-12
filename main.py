import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout

from Entity.Game import Game
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

        self.interrupt_to_detect_hand_counter = 0
        self.structure_is_created = False

        self.thread = VideoThread(Constants.VIDEO_STREAM_ADDRESS)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, frame):
        self.interrupt_to_detect_hand_counter = (self.interrupt_to_detect_hand_counter + 1) % Constants.DETECTION_RATE
        if self.interrupt_to_detect_hand_counter == 0:
            self.game.detect_gesture(frame)
            if self.game.player.is_visible:
                self.game.clear_last_surface()
                self.game.draw_surface()

        self.game.move_ball()
        self.set_frame_within_label(frame)

    def set_frame_within_label(self, frame):
        self.game.blend(frame)
        qt_img = convert_cv_qt(self.game.get_drawer_output())
        self.image_label.setPixmap(qt_img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
