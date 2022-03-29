from Entity.Block import Block


class Board:
    def __init__(self, board_size):
        self.size = board_size
        self.blocks = [[Block((j + 1) + (i * self.size[1]), (i + 1, j + 1))
                        for j in range(self.size[1])] for i in range(self.size[0])]
