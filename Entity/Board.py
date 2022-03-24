from Entity.Block import Block


class Board:
    def __init__(self, board_size):
        self.size = board_size
        self._blocks = [[Block((j + 1) + (i * self.size[0]), (i + 1, j + 1))
                         for j in range(self.size[0])] for i in range(self.size[1])]
