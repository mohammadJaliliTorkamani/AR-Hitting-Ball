from Entity.Board import Board
from Entity.Player import Player
from Utils.HandDetector import HandDetector


class Game:
    def __init__(self, blocks_size, display_size):
        (self.display_width, self.display_height) = display_size
        self.board = Board(blocks_size)
        self.player = Player()
        self.detector = HandDetector()
        self.is_playing = False

    def draw_game_structure(self):
        print("Drawn!!")
        pass

    def detect_gesture(self, cv_img):
        visibility, hand_position, hand_status = self.detector.detect_gesture(cv_img)
        self.player.visible = visibility
        self.player.hand_status = hand_status
        self.player.position = hand_position

    def get_player_hand_status(self):
        return self.player.hand_status

    def player_is_visible(self):
        return self.player.is_visible
