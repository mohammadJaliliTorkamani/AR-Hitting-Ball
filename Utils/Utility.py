import cv2
import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Utils import Constants

pygame.mixer.init()
sound = pygame.mixer.Sound(Constants.BEEP_SOUND_ADDRESS)


def convert_cv_qt(frame, display_width = Constants.SCREEN_WIDTH, display_height = Constants.SCREEN_HEIGHT):
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
    p = convert_to_qt_format.scaled(display_width, display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


def play_beep():
    sound.play()
