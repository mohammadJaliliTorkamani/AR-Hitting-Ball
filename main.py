import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout

from Entity.Game import Game
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

        self.drawer = Drawer()
        self.game = Game((4, 9), (self.display_width, self.display_height), self.drawer)

        self.interrupt_to_detect_hand_counter = 0
        self.structure_is_created = False

        self.thread = VideoThread("https://192.168.1.155:8080/video", self.display_width, self.display_height)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        if not self.structure_is_created:
            self.game.draw_game_structure()
            self.structure_is_created = True

        self.interrupt_to_detect_hand_counter = (self.interrupt_to_detect_hand_counter + 1) % 3
        if self.interrupt_to_detect_hand_counter == 0:
            self.game.detect_gesture(cv_img)
            if self.game.player.is_visible:
                self.game.clear_last_surface()
                self.game.draw_surface()

        if self.game.surface.current_x is not None:  # is True for the first detection
            self.play_in_step()
        self.show_cv_img_in_frame(cv_img)

    def show_cv_img_in_frame(self, cv_img):
        self.drawer.blend(cv_img)
        qt_img = convert_cv_qt(self.drawer.output, self.display_width, self.display_height)
        self.image_label.setPixmap(qt_img)

    def play_in_step(self):
        self.game.ball.last_position = self.game.ball.current_position
        if not self.game.game_begun:
            self.game.game_begun = True
            self.game.ball.current_position = (
                self.game.surface.current_x + int(self.game.surface.length / 2), self.game.surface.y - 10)

        # if self.game.ball.position[0] == self.game.display_width:
        #     ##calculate reflex_position and
        #     self.drawer.clear(self.game.ball.last_position)
        #     self.drawer.draw(self.game.ball.current_position, 1)
        #
        #     pass
        # elif self.game.ball.position[0] == 0:
        #     ##calculate reflex_position and
        #     self.drawer.clear(self.game.ball.position)
        #     self.drawer.draw(self.game.ball.current_position, 1)
        #     pass
        # elif self.game.ball.position[1] == 0:
        #     ##calculate reflex_position and
        #     self.drawer.clear(self.game.ball.position)
        #     self.drawer.draw(self.game.ball.current_position, 1)
        #     pass
        # elif self.game.ball.position[1] == self.game.display_height:
        #     print("User lost!")
        #     pass
        # elif (self.game.ball.position[0] == self.game.player.current_position[0]) and (
        #         self.game.ball.position[1] == self.game.player.current_position[1]):
        #     ###REFLECT ON SURFACE
        #     pass
        # else:
        #     # CALCULATE NEXT POSITION FREELY AND PLACE THE BALL THERE
        #     pass
        self.drawer.draw(self.game.ball.current_position, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
