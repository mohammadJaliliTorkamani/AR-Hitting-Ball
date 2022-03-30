import cv2


class Drawer:
    SURFACE_DRAWING = 0
    BALL_DRAWING = 1
    BLOCK_DRAWING = 2

    PIXEL_DIMENSION = 10

    _BLOCK_COLOR = (255, 255, 0)
    _BALL_COLOR = (0, 255, 255)
    _SURFACE_COLOR = (0, 102, 255)

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
                cv2.circle(self.output, point, Drawer.PIXEL_DIMENSION, color, cv2.FILLED)
            else:
                start_pos = (point[0] - int(Drawer.PIXEL_DIMENSION / 2), point[1] - int(Drawer.PIXEL_DIMENSION / 2))
                end_pos = (point[0] + int(Drawer.PIXEL_DIMENSION / 2), point[1] + int(Drawer.PIXEL_DIMENSION / 2))
                cv2.rectangle(self.output, start_pos, end_pos, color, cv2.FILLED)

    def clear(self, pos):
        if pos in self._mask:
            del self._mask[pos]
            return True
        else:
            return False
