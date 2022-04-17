from dataclasses import dataclass

from Entity.Drawable import Drawable
from Utils import Constants


@dataclass
class Surface(Drawable):
    length: int = Constants.SURFACE_LENGTH

    def get_end_x(self):
        return self.current_position[0] + self.length
