from random import choice

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
                block = Block(position_in_board=(i + 1, j + 1))
                block.color = choice(Constants.BLOCK_COLORS)
                row.append(block)
            self.blocks_list.append(row)
