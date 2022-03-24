from Entity.Board import Board
from Entity.Player import Player


class Game:
    def __init__(self, blocks_size, display_size):
        (self.display_width, self.display_height) = display_size
        self.board = Board(blocks_size)
        self.player = Player()
        self.player_is_visible = False
        self.is_playing = False

    def draw_game_structure(self):
        pass

    def detect_gesture(self):
        pass

    def get_player_hand_status(self):
        pass

