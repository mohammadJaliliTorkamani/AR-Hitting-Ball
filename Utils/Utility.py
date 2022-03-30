import cv2
import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

pygame.mixer.init()
sound = pygame.mixer.Sound('/usr/share/sounds/freedesktop/stereo/bell.oga')


def convert_cv_qt(cv_img, display_width, display_height):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
    p = convert_to_qt_format.scaled(display_width, display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


def play_beep():
    sound.play()
