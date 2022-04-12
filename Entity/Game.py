import itertools

from Entity.Ball import Ball
from Entity.Board import Board
from Entity.Player import Player
from Entity.Surface import Surface
from Utils import Constants
from Utils.Drawer import Drawer
from Utils.Utility import play_beep


class Game:
    def __init__(self, blocks_size, display_size=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)):
        (self.display_width, self.display_height) = display_size
        self.blocks_board = Board(blocks_size)
        self.player = Player()
        self.ball = Ball()
        self.surface = Surface(self.display_height - 100)
        self.drawer = Drawer()
        self.game_begun = False
        self.game_status = None

    def draw_game_structure(self):
        for block in itertools.chain.from_iterable(self.blocks_board.blocks):
            row, col = block.position[0], block.position[1]
            block.position_in_frame = (
                int(col / (self.blocks_board.size[1] + 1) * self.display_width) - int(block.length / 2),
                int(0.4 * (row / (self.blocks_board.size[0] + 1)) * self.display_height) + 10)
            self.draw_block(block)

    def detect_gesture(self, frame):
        visible, position = self.player.detect_gesture(frame)
        if visible and (position[0] + self.surface.length <= self.display_width) and (position[0] >= 0):
            self.player.is_visible = visible
            self.player.last_position = self.player.current_position
            self.player.current_position = position
            self.surface.last_x = self.surface.current_x
            self.surface.current_x = position[0]
            if not self.game_begun:
                self.game_begun = True
                self.ball.current_position = (
                    self.surface.current_x + int(self.surface.length / 2), self.surface.y - 10)

    def clear_last_surface(self):
        if self.surface.last_x is not None:  # is True for the first detection
            [self.drawer.clear((self.surface.last_x + i, self.surface.y)) for i in range(self.surface.length)]

    def draw_surface(self):
        [self.drawer.draw((self.surface.current_x + i, self.surface.y), Drawer.SURFACE_DRAWING) for i in
         range(self.surface.length)]

    def draw_new_ball(self):
        self.drawer.clear(self.ball.last_position)
        self.drawer.draw(self.ball.current_position, Drawer.BALL_DRAWING)

    def remove_block(self, block):
        for k in range(block.length):
            block_x = int(block.position[1] / (
                    self.blocks_board.size[1] + 1) * self.display_width) + k - int(block.length / 2)
            block_y = int(0.4 * (block.position[0] / (
                    self.blocks_board.size[0] + 1)) * self.display_height) + 10
            self.drawer.clear((block_x, block_y))

    def move_ball(self):
        if self.surface.current_x is None or self.game_status is not None:
            return

        self.ball.last_position = self.ball.current_position

        # BLOCK COLLISION STATE CHECK
        for block in filter(lambda block: block.alive, itertools.chain.from_iterable(self.blocks_board.blocks)):
            if (block.position_in_frame[0] <= self.ball.current_position[0] <=
                block.get_end_position_in_frame()[0]) and (
                    self.ball.current_position[1] == block.position_in_frame[1]):
                block.alive = False
                self.remove_block(block)
                self.ball.is_moving_up = not self.ball.is_moving_up
                play_beep()
                self.adjust_winning_status()

        # HORIZONTAL COLLISION CHECK
        if (self.ball.current_position[0] == self.display_width) or (self.ball.current_position[0] == 0):
            self.ball.is_moving_right = not self.ball.is_moving_right
            play_beep()

        # VERTICAL (TOP SIDE) COLLISION CHECK
        elif self.ball.current_position[1] == 0:
            self.ball.is_moving_up = False
            play_beep()

        # VERTICAL (BOTTOM SIDE) COLLISION CHECK
        elif self.ball.current_position[1] == self.display_height:
            self.game_status = False
            play_beep()
            play_beep()

        elif ((self.surface.current_x <= self.ball.current_position[0] <= self.surface.get_end_x())
              and ((self.ball.current_position[1] + Constants.PIXEL_DIMENSION) == self.surface.y)):
            self.ball.is_moving_up = True
            play_beep()

        new_pos_x = (self.ball.current_position[0] + 1) if self.ball.is_moving_right \
            else (self.ball.current_position[0] - 1)
        new_pos_y = (self.ball.current_position[1] - 1) if self.ball.is_moving_up \
            else (self.ball.current_position[1] + 1)

        self.ball.current_position = (new_pos_x, new_pos_y)
        self.draw_new_ball()

    def draw_block(self, block):
        for k in range(block.length):
            self.drawer.draw((block.position_in_frame[0] + k, block.position_in_frame[1]), Drawer.BLOCK_DRAWING)

    def blend(self, frame):
        self.drawer.blend(frame)

    def get_drawer_output(self):
        return self.drawer.output

    def adjust_winning_status(self):
        if len(list(enumerate(
                filter(lambda block: block.alive, itertools.chain.from_iterable(self.blocks_board.blocks))))) == 0:
            self.game_status = True
