from Entity.Ball import Ball
from Entity.Board import Board
from Entity.Player import Player
from Entity.Surface import Surface
from Utils.HandDetector import HandDetector


class Game:
    def __init__(self, blocks_size, display_size, drawer):
        (self.display_width, self.display_height) = display_size
        self.blocks_board = Board(blocks_size)
        self.player = Player()
        self.ball = Ball()
        self.surface = Surface(800)
        self.drawer = drawer
        self.detector = HandDetector()
        self.game_begun = False

    def draw_game_structure(self):
        for block_row in self.blocks_board.blocks:
            for block in block_row:
                row = block.position[0]
                col = block.position[1]
                for k in range(block.length):
                    self.drawer.draw(
                        (int(col / (self.blocks_board.size[1] + 1) * self.display_width) + k - int(block.length / 2),
                         int(0.4 * (row / (self.blocks_board.size[0] + 1)) * self.display_height) + 10), 2)

    def detect_gesture(self, cv_img):
        visible, position = self.detector.detect_gesture(cv_img)
        if visible and (position[0] + self.surface.length <= self.display_width) and (position[0] >= 0):
            self.player.is_visible = visible
            self.player.last_position = self.player.current_position
            self.player.current_position = position
            self.surface.last_x = self.surface.current_x
            self.surface.current_x = position[0]

    def clear_last_surface(self):
        if self.surface.last_x is not None:  # is True for the first detection
            for i in range(self.surface.length):
                self.drawer.clear((self.surface.last_x + i, self.surface.y))

    def draw_surface(self):
        for i in range(self.surface.length):
            self.drawer.draw((self.surface.current_x + i, self.surface.y), 0)

    def clear_last_ball(self):
        self.drawer.clear(self.ball.last_position)

    def draw_ball(self):
        self.drawer.draw(self.ball.current_position, 1)

    def remove_block(self, block_x, block_y):
        print("REMOVING")
        self.drawer.clear((block_x, block_y))
