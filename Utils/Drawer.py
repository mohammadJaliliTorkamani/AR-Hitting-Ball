import cv2


class Drawer:
    SURFACE_DRAWING = 0
    BALL_DRAWING = 1
    BLOCK_DRAWING = 2

    _PIXEL_DIMENSION = 10

    def __init__(self):
        self._mask = {}
        self.output = None

    def draw(self, position, mode):
        self._mask[position] = mode
        return self

    def blend(self, cv_img):
        self.output = cv_img
        for (point, value) in self._mask.items():
            color = (250, 253, 15) if value == 0 else ((0, 0, 255) if value == 1 else (255, 0, 0))
            start_pos = (point[0] - int(Drawer._PIXEL_DIMENSION / 2), point[1] - int(Drawer._PIXEL_DIMENSION / 2))
            end_pos = (point[0] + int(Drawer._PIXEL_DIMENSION / 2), point[1] + int(Drawer._PIXEL_DIMENSION / 2))
            cv2.rectangle(self.output, start_pos, end_pos, color, cv2.FILLED)

    def clear(self, pos):
        if pos in self._mask:
            del self._mask[pos]
            return True
        else:
            return False
