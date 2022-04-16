from Entity.Drawable import Drawable
from Utils import Constants


class Surface(Drawable):
    def __init__(self, color, current_position=(-1, -1), last_position=(-1, -1)):
        super().__init__(color, current_position, last_position)
        self.length = Constants.SURFACE_LENGTH

    def get_end_x(self):
        return self.current_position[0] + self.length
