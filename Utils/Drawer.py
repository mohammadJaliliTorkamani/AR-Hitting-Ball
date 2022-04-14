import cv2

from Entity.Block import Block
from Entity.Surface import Surface
from Utils import Constants


class Drawer:
    def __init__(self):
        self._mask = {}
        self.output = None

    def draw(self, drawable):
        if (type(drawable) is Surface) or (type(drawable) is Block):
            for i in range(drawable.length):
                self._mask[(drawable.current_position[0] + i, drawable.current_position[1])] = drawable.color
        else:
            self._mask[drawable.current_position] = drawable.color

        return self

    def blend(self, frame):
        self.output = frame
        for (point, value) in self._mask.items():
            cv2.circle(self.output, point, Constants.PIXEL_DIMENSION, value, cv2.FILLED)

    def clear(self, position):
        if position in self._mask:
            del self._mask[position]
            return True
        else:
            return False
