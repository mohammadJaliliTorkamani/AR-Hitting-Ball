import cv2
from pygame import mixer
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from numpy import ndarray

from Utils import Constants

mixer.init()
sound = mixer.Sound(Constants.BEEP_SOUND_ADDRESS)


def convert_cv_qt(frame: ndarray, display_width: int = Constants.SCREEN_WIDTH,
                  display_height: int = Constants.SCREEN_HEIGHT):
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, channel = rgb_image.shape
    convert_to_qt_format = QtGui.QImage(rgb_image.data, width, height, channel * width, QtGui.QImage.Format_RGB888)
    image = convert_to_qt_format.scaled(display_width, display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(image)


def play_beep():
    sound.play()
