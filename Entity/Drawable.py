from dataclasses import dataclass


@dataclass
class Drawable:
    color: tuple = (255, 255, 255)
    current_position: tuple = (-1, -1)
    last_position: tuple = (-1, -1)
    visible: bool = True
