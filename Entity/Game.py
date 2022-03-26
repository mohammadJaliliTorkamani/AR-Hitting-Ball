from Entity.Board import Board
from Entity.Player import Player
from Utils.HandDetector import HandDetector


class Game:
    def __init__(self, blocks_size, display_size, drawer):
        (self.display_width, self.display_height) = display_size
        self.board = Board(blocks_size)
        self.player = Player()
        self.drawer = drawer
        self.detector = HandDetector()
        self.is_playing = False

    def draw_game_structure(self):
        for i in range(self.board.size[1]):
            for j in range(self.board.size[0]):
                self.drawer.draw((int(j / self.board.size[0] * self.display_width + 100),     int(0.3*i / self.board.size[1] * self.display_height) + 10), 2)

    def detect_gesture(self, cv_img):
        visibility, hand_position = self.detector.detect_gesture(cv_img)
        self.player.is_visible = visibility
        self.player.position = hand_position
