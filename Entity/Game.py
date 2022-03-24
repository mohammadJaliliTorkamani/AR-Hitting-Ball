from Entity.Board import Board
from Entity.Player import Player


class Game:
    def __init__(self, blocks_size, display_size):
        (self.display_width, self.display_height) = display_size
        self.board = Board(blocks_size)
        self.player = Player()
        self.is_playing = False

    def draw_game_structure(self):
        pass

    def detect_gesture(self):
        self.player.visible = True
        self.player.hand_status = 1

    def get_player_hand_status(self):
        return self.player.hand_status

    def player_is_visible(self):
        return self.player.is_visible
