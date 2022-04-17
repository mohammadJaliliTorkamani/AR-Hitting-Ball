import cv2
from numpy import ndarray

from Entity.Block import Block
from Entity.Drawable import Drawable
from Entity.Surface import Surface
from Utils import Constants


class Drawer:
    def __init__(self):
        self._mask = {}
        self.output = None

    def draw(self, drawable: Drawable):
        if (isinstance(drawable, Surface)) or (isinstance(drawable, Block)):
            for i in range(drawable.length):
                self._mask[
                    (drawable.current_position[0] + i, drawable.current_position[1])
                ] = drawable.color
        else:
            self._mask[drawable.current_position] = drawable.color

        return self

    def blend(self, frame: ndarray):
        self.output = frame

        for (point, value) in self._mask.items():
            cv2.circle(self.output, point, Constants.PIXEL_DIMENSION, value, cv2.FILLED)

    def clear(self, position: tuple) -> bool:
        if position in self._mask:
            del self._mask[position]
            return True
        return False
