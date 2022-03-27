import cv2


class Drawer:
    def __init__(self):
        self._mask = {}
        self.output = None

    def draw(self, position, mode):  # modes: Player's Surface : 0 , Ball : 1, Block : 2
        self._mask[position] = mode
        return self

    def blend(self, cv_img):
        self.output = cv_img
        for (point, value) in self._mask.items():
            color = (250, 253, 15) if value == 0 else ((0, 0, 255) if value == 1 else (255, 0, 0))
            start_pos = (point[0] - 5, point[1] - 5)
            end_pos = (point[0] + 5, point[1] + 5)
            cv2.rectangle(self.output, start_pos, end_pos, color, cv2.FILLED)

    def clear(self, pos):
        if pos in self._mask:
            del self._mask[pos]
