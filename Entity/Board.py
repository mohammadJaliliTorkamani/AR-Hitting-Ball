import random

from Entity.Block import Block
from Utils import Constants


class Board:
    def __init__(self, board_size: tuple):
        self.size = board_size
        self.blocks_list = []
        self._init_blocks()

    def _init_blocks(self):
        for i in range(self.size[0]):
            row = []
            for j in range(self.size[1]):
                block_color = Constants.BLOCK_COLORS[random.randint(0, len(Constants.BLOCK_COLORS) - 1)]
                row.append(Block(position_in_board=(i + 1, j + 1), color=block_color))
            self.blocks_list.append(row)
