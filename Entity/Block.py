from Entity.Drawable import Drawable
from Utils import Constants


class Block(Drawable):
    def __init__(self, position_in_board: tuple):
        self.length = Constants.BLOCK_LENGTH
        self.position_in_board = position_in_board
        self.alive = True

    def get_end_position_in_frame(self) -> tuple:
        return self.current_position[0] + self.length, self.current_position[1]
