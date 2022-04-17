import cv2
import numpy
import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Utils import Constants

pygame.mixer.init()
sound = pygame.mixer.Sound(Constants.BEEP_SOUND_ADDRESS)


def convert_cv_qt(frame: numpy.ndarray, display_width: int = Constants.SCREEN_WIDTH,
                  display_height: int = Constants.SCREEN_HEIGHT):
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, channel = rgb_image.shape
    convert_to_qt_format = QtGui.QImage(rgb_image.data, width, height, channel * width, QtGui.QImage.Format_RGB888)
    image = convert_to_qt_format.scaled(display_width, display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(image)


def play_beep():
    sound.play()
