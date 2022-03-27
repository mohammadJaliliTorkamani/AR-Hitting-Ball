from Entity.Ball import Ball
from Entity.Board import Board
from Entity.Player import Player
from Utils.HandDetector import HandDetector


class Game:
    def __init__(self, blocks_size, display_size, drawer):
        (self.display_width, self.display_height) = display_size
        self.board = Board(blocks_size)
        self.player = Player()
        self.ball = Ball()
        self.drawer = drawer
        # self.detector = HandDetector()
        self.game_begun = False

    def draw_game_structure(self):
        for i in range(self.board.size[1]):
            for j in range(self.board.size[0]):
                self.drawer.draw((int(j / self.board.size[0] * self.display_width + 100),
                                  int(0.3 * i / self.board.size[1] * self.display_height) + 10), 2)

    # def play_in_step(self):
    #     if not self.game_begun:
    #         self.ball.position = self.player.position
    #
    #     if self.ball.position == right_side:
    #         ##calculate reflex_position
    #         pass
    #     elif self.ball.position == left_side:
    #         ##calculate reflex_position
    #         pass
    #     elif self.ball.position == top_side:
    #         ##calculate reflex_position
    #         pass
    #     elif self.ball.position == bottom_side:
    #         ##user lost!
    #         pass
    #     elif self.ball.position == surface:
    #         ###REFLECT
    #         pass
    #     else:
    #         #CALCULATE NEXT POSITION AND PLACE THE BALL THERE
