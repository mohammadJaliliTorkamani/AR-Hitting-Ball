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
        for i in range(self.blocks_board.size[0]):
            for j in range(self.blocks_board.size[1]):
                for k in range(30):
                    self.drawer.draw((int((j+1) / (self.blocks_board.size[1]+1) * self.display_width) + k,
                                      int(0.3 * ((i+1) / (self.blocks_board.size[0]+1)) * self.display_height) + 10), 2)

    def detect_gesture(self, cv_img):
        visible, position = self.detector.detect_gesture(cv_img)
        print(position)
        self.player.is_visible = visible
        if visible and (position[0] + self.surface.length <= self.display_width) and (position[0] >= 0):
            self.player.last_position = self.player.current_position
            self.player.current_position = position
            self.surface.x = position[0]

    def clear_last_surface(self):
        for i in range(self.surface.length):
            self.drawer.clear((self.player.last_position[0] + i, self.surface.y))

    def draw_surface(self):
        for i in range(self.surface.length):
            self.drawer.draw((self.surface.x + i, self.surface.y), 0)
