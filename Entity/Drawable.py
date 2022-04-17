from dataclasses import dataclass


@dataclass
class Drawable:
    color: tuple
    current_position: tuple = (-1, -1)
    last_position: tuple = (-1, -1)
