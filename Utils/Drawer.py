import cv2


class Drawer:
    def __init__(self):
        self._mask = {}
        self.output = None
        self.pixel_dim = 10

    def draw(self, position, mode):  # modes: Player's Surface : 0 , Ball : 1, Block : 2
        self._mask[position] = mode
        return self

    def blend(self, cv_img):
        self.output = cv_img
        for (point, value) in self._mask.items():
            color = (250, 253, 15) if value == 0 else ((0, 0, 255) if value == 1 else (255, 0, 0))
            start_pos = (point[0] - int(self.pixel_dim/2), point[1] - int(self.pixel_dim/2))
            end_pos = (point[0] + int(self.pixel_dim/2), point[1] + int(self.pixel_dim/2))
            cv2.rectangle(self.output, start_pos, end_pos, color, cv2.FILLED)

    def clear(self, pos):
        if pos in self._mask:
            del self._mask[pos]
            return True
        else:
            return False
