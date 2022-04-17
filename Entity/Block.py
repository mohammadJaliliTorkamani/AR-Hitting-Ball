from Entity.Drawable import Drawable
from Utils import Constants


class Block(Drawable):
    def __init__(self, block_id: int, position_in_board: tuple, color: tuple = (255, 255, 255),
                 current_position: tuple = (-1, -1)):
        super().__init__(color, current_position)
        self.id = block_id
        self.length = Constants.BLOCK_LENGTH
        self.position_in_board = position_in_board
        self.alive = True
        self.hidden = False

    def get_end_position_in_frame(self) -> tuple:
        return self.current_position[0] + self.length, self.current_position[1]
