import cv2

from Utils import Constants


class Drawer:
    SURFACE_DRAWING = 0
    BALL_DRAWING = 1
    BLOCK_DRAWING = 2

    _BLOCK_COLOR = Constants.BLOCK_COLOR
    _BALL_COLOR = Constants.BALL_COLOR
    _SURFACE_COLOR = Constants.SURFACE_COLOR

    def __init__(self):
        self._mask = {}
        self.output = None

    def draw(self, position, mode):
        self._mask[position] = mode
        return self

    def blend(self, cv_img):
        self.output = cv_img
        for (point, value) in self._mask.items():
            color = Drawer._SURFACE_COLOR if value == Drawer.SURFACE_DRAWING else (
                Drawer._BALL_COLOR if value == Drawer.BALL_DRAWING else Drawer._BLOCK_COLOR)

            if (value == Drawer.BALL_DRAWING) or (value == Drawer.SURFACE_DRAWING):
                cv2.circle(self.output, point, Constants.PIXEL_DIMENSION, color, cv2.FILLED)
            else:
                start_pos = (point[0] - int(Constants.PIXEL_DIMENSION / 2), point[1] - int(Constants.PIXEL_DIMENSION / 2))
                end_pos = (point[0] + int(Constants.PIXEL_DIMENSION / 2), point[1] + int(Constants.PIXEL_DIMENSION / 2))
                cv2.rectangle(self.output, start_pos, end_pos, color, cv2.FILLED)

    def clear(self, pos):
        if pos in self._mask:
            del self._mask[pos]
            return True
        else:
            return False
