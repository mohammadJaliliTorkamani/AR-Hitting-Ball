from dataclasses import dataclass

from Entity.Drawable import Drawable


@dataclass
class Ball(Drawable):
    is_moving_up: bool = True
    is_moving_right: bool = True
