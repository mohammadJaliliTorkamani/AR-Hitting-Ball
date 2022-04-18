from sys import argv, exit

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from numpy import ndarray

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

        self.thread = VideoThread(Constants.VIDEO_STREAM_ADDRESS)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(ndarray)
    def update_image(self, frame: ndarray):
        if self.game.can_detect_hands():
            self.game.detect_gesture(frame)
            if self.game.is_visible_player():
                self.game.redraw_surface()

        self.game.move_ball()
        self.game.blend(frame)
        self.game.draw_status_text()

        self.image_label.setPixmap(convert_cv_qt(frame))


if __name__ == "__main__":
    q_app = QApplication(argv)
    app = App()
    app.show()
    exit(q_app.exec_())
