from itertools import chain
from random import randint

from numpy import ndarray

from Entity.Ball import Ball
from Entity.Block import Block
from Entity.Board import Board
from Entity.Player import Player
from Entity.Surface import Surface
from Thread.RepeatedTask import RepeatedTimer
from Utils import Constants
from Utils.Drawer import Drawer
from Utils.Utility import play_beep


class Game:
    def __init__(self, blocks_size, display_size=(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)):
        (self.display_width, self.display_height) = display_size
        self.blocks_board = Board(blocks_size)
        self.player = Player()
        self.ball = Ball(color=Constants.BALL_COLOR)
        self.surface = Surface(color=Constants.SURFACE_COLOR, current_position=(-1, self.display_height - 100))
        self.drawer = Drawer()
        self.game_status = None
        self._hidden_block_candidate = None
        RepeatedTimer(Constants.BLOCK_HIDE_RATE, self.hide_blocks)

    def hide_blocks(self):
        if self._hidden_block_candidate is not None:
            self.toggle_block_visibility(self._hidden_block_candidate)

        alive_shown_blocks = list(
            filter(lambda block: block.alive and not block.hidden, chain.from_iterable(self.blocks_board.blocks_list)))
        self._hidden_block_candidate = alive_shown_blocks[randint(0, len(alive_shown_blocks) - 1)]
        self.toggle_block_visibility(self._hidden_block_candidate)

    def draw_game_structure(self):
        for block in filter(lambda block: block.alive and not block.hidden,
                            chain.from_iterable(self.blocks_board.blocks_list)):
            row, col = block.position_in_board[0], block.position_in_board[1]
            block.current_position = (
                int(col / (self.blocks_board.size[1] + 1) * self.display_width) - int(block.length / 2),
                int(Constants.BLOCK_VERTICAL_COEFFICIENT * (row / (
                        self.blocks_board.size[0] + 1)) * self.display_height) + Constants.BLOCK_VERTICAL_MARGIN)
            self.draw_block(block)

    def detect_gesture(self, frame: ndarray):
        visible, position = self.player.detect_gesture(frame)
        if visible and (position[0] + self.surface.length <= self.display_width) and (position[0] >= 0):
            self.player.is_visible = visible
            self.player.last_position = self.player.current_position
            self.player.current_position = position

            self.surface.last_position = self.surface.current_position
            self.surface.current_position = (position[0], self.surface.current_position[1])

            if self.ball.current_position[0] == -1:
                self.ball.current_position = (
                    self.surface.current_position[0] + int(self.surface.length / 2),
                    self.surface.current_position[1] - Constants.PIXEL_DIMENSION)

    def clear_last_surface(self):
        if self.surface.last_position[0] != -1:  # is True for the first detection
            for i in range(self.surface.length):
                self.drawer.clear((self.surface.last_position[0] + i, self.surface.current_position[1]))

    def draw_new_ball(self):
        self.drawer.clear(self.ball.last_position)
        self.drawer.draw(self.ball)

    def clear_block(self, block: Block):
        for k in range(block.length):
            block_position = int(
                block.position_in_board[1] / (self.blocks_board.size[1] + 1) * self.display_width) + k - int(
                block.length / 2), int(
                Constants.BLOCK_VERTICAL_COEFFICIENT * (block.position_in_board[0] / (
                        self.blocks_board.size[0] + 1)) * self.display_height) + Constants.BLOCK_VERTICAL_MARGIN
            self.drawer.clear(block_position)

    def move_ball(self):
        if (self.surface.current_position[0] == -1) or (self.game_status is not None):
            return

        self.ball.last_position = self.ball.current_position

        # BLOCK COLLISION STATE CHECK
        for block in filter(lambda block: block.alive and not block.hidden,
                            chain.from_iterable(self.blocks_board.blocks_list)):
            if self.ball.is_moving_up:
                if (block.current_position[0] <= self.ball.current_position[0] <= block.get_end_position_in_frame()[
                    0]) and \
                        ((block.current_position[1] - Constants.PIXEL_DIMENSION) <= (
                                self.ball.current_position[1] - Constants.PIXEL_DIMENSION) <= (
                                 block.current_position[1] + Constants.PIXEL_DIMENSION)):
                    block.alive = False
                    self.clear_block(block)
                    self.ball.is_moving_up = not self.ball.is_moving_up
                    play_beep()
                    self.adjust_winning_status()
            else:
                if (block.current_position[0] <= self.ball.current_position[0] <= block.get_end_position_in_frame()[0]) \
                        and \
                        ((block.current_position[1] - Constants.PIXEL_DIMENSION) <=
                         (self.ball.current_position[1] + Constants.PIXEL_DIMENSION) <=
                         (block.current_position[1] + Constants.PIXEL_DIMENSION)):
                    block.alive = False
                    self.clear_block(block)
                    self.ball.is_moving_up = not self.ball.is_moving_up
                    play_beep()
                    self.adjust_winning_status()

        # HORIZONTAL COLLISION CHECK
        if (self.ball.current_position[0] >= self.display_width) or (self.ball.current_position[0] <= 0):
            self.ball.is_moving_right = not self.ball.is_moving_right
            play_beep()

        # VERTICAL (TOP SIDE) COLLISION CHECK
        elif self.ball.current_position[1] <= 0:
            self.ball.is_moving_up = False
            play_beep()

        # VERTICAL (BOTTOM SIDE) COLLISION CHECK
        elif self.ball.current_position[1] >= self.display_height:
            self.game_status = False
            play_beep()

        elif ((self.surface.current_position[0] <= self.ball.current_position[0] <= self.surface.get_end_x())
              and ((self.ball.current_position[1] + Constants.PIXEL_DIMENSION) >=
                   self.surface.current_position[1] - Constants.PIXEL_DIMENSION)):
            self.ball.is_moving_up = True
            play_beep()

        new_pos_x = (self.ball.current_position[0] + Constants.BALL_MOVEMENT_STEP) if self.ball.is_moving_right else (
                self.ball.current_position[0] - Constants.BALL_MOVEMENT_STEP)
        new_pos_y = (self.ball.current_position[1] - Constants.BALL_MOVEMENT_STEP) if self.ball.is_moving_up \
            else (self.ball.current_position[1] + Constants.BALL_MOVEMENT_STEP)

        self.ball.current_position = (new_pos_x, new_pos_y)
        self.draw_new_ball()

    def draw_block(self, block: Block):
        for _ in range(block.length):
            self.drawer.draw(block)

    def blend(self, frame: ndarray):
        self.drawer.blend(frame)

    def get_drawer_output(self) -> ndarray:
        return self.drawer.output

    def adjust_winning_status(self):
        if len(list(enumerate(
                filter(lambda block: block.alive, chain.from_iterable(self.blocks_board.blocks_list))))) == 0:
            self.game_status = True

    def toggle_block_visibility(self, block: Block):
        block.hidden = not block.hidden
        if block.hidden:
            self.clear_block(block)
        else:
            self.draw_block(block)

    def draw_surface(self):
        self.drawer.draw(self.surface)
