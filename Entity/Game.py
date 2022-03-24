from Entity.Board import Board


class Game:
    def __init__(self, blocks_size, display_size):
        (self.display_width, self.display_height) = display_size
        self.board = Board(blocks_size)
