import random

from Entity.Block import Block
from Utils import Constants


class Board:
    def __init__(self, board_size: tuple):
        self.size = board_size
        self.blocks = []
        for i in range(self.size[0]):
            row = []
            for j in range(self.size[1]):
                block_color = Constants.BLOCK_COLORS[random.randint(0, len(Constants.BLOCK_COLORS) - 1)]
                row.append(
                    Block(block_id=(j + 1) + (i * self.size[1]), position_in_board=(i + 1, j + 1), color=block_color))
            self.blocks.append(row)
