from itertools import chain
from random import choice

import cv2
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
        self.ball = Ball(color=Constants.BALL_COLOR, visible=False)
        self.surface = Surface(visible=False, color=Constants.SURFACE_COLOR,
                               current_position=(-1, self.display_height - Constants.SURFACE_BOTTOM_MARGIN))
        self.drawer = Drawer()
        self.is_winner = None
        self._hidden_block_candidate = None
        RepeatedTimer(Constants.BLOCK_HIDE_RATE, self.hide_blocks)
        self.can_detect_hand = False
        self.draw_shown_alive_blocks()

        self.hand_detection_timer = RepeatedTimer(Constants.HAND_DETECTION_RATE, self.invert_can_detect_hand)

    def hide_blocks(self):
        if self._hidden_block_candidate is not None:
            self.toggle_block_visibility(self._hidden_block_candidate)

        alive_shown_blocks = list(filter(lambda block: block.alive and block.visible,
                                         chain.from_iterable(self.blocks_board.blocks_list)))
        self._hidden_block_candidate = choice(alive_shown_blocks)
        self.toggle_block_visibility(self._hidden_block_candidate)

    def invert_can_detect_hand(self):
        self.can_detect_hand = not self.can_detect_hand

    def can_detect_hands(self):
        return self.can_detect_hand

    def draw_shown_alive_blocks(self):
        for block in filter(lambda block: block.alive and block.visible,
                            chain.from_iterable(self.blocks_board.blocks_list)):
            self.draw_block(block)

    def redraw_surface(self):
        self.clear_last_surface()
        self.draw_surface()

    def draw_status_text(self):
        cv2.putText(self.get_drawer_output(), "Game Status: " +
                    ("Playing" if self.is_winner is None else ("You win" if self.is_winner else "You lose")),
                    (int(Constants.SCREEN_WIDTH / 2) - 80, Constants.SCREEN_HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255) if self.is_winner else (255, 100, 40), thickness=2)

    def detect_gesture(self, frame: ndarray):
        visible, position = self.player.detect_gesture(frame)
        if visible and (position[0] + self.surface.length <= self.display_width) and (position[0] >= 0):
            self.player.is_visible = visible
            self.player.last_position = self.player.current_position
            self.player.current_position = position

            self.surface.visible = True
            self.surface.last_position = self.surface.current_position
            self.surface.current_position = (position[0], self.surface.current_position[1])

            if not self.ball.visible:
                self.ball.visible = True
                self.ball.current_position = (
                    self.surface.current_position[0] + int(self.surface.length / 2),
                    self.surface.current_position[1] - Constants.PIXEL_DIMENSION)

    def clear_last_surface(self):
        for i in range(self.surface.length):
            self.drawer.clear((self.surface.last_position[0] + i, self.surface.current_position[1]))

    def draw_new_ball(self):
        self.drawer.clear(self.ball.last_position)
        self.drawer.draw(self.ball)

    def clear_block(self, block: Block):
        block.visible = False
        for k in range(block.length):
            block_position = int(
                block.position_in_board[1] / (self.blocks_board.size[1] + 1) * self.display_width) + k - int(
                block.length / 2), int(
                Constants.BLOCK_VERTICAL_COEFFICIENT * (block.position_in_board[0] / (
                        self.blocks_board.size[0] + 1)) * self.display_height) + Constants.BLOCK_VERTICAL_MARGIN
            self.drawer.clear(block_position)

    def move_ball(self):
        if not self.ball.visible:
            return

        self.ball.last_position = self.ball.current_position

        for block in filter(lambda block: block.alive and block.visible,
                            chain.from_iterable(self.blocks_board.blocks_list)):
            if self.ball.is_hit_block(block):
                block.alive = False
                self.clear_block(block)
                self.ball.toggle_moving_up()
                play_beep()
                self.adjust_winning_status()

        if not self.ball.is_horizontally_aligned(self.display_width):
            self.ball.toggle_moving_right()
            play_beep()

        elif not self.ball.is_vertically_in_range(self.display_height):
            self.is_winner = False
            self.ball.visible = False
            self.drawer.clear(self.ball.current_position)

        elif not self.ball.is_vertically_top_aligned():
            self.ball.is_moving_up = False
            play_beep()

        elif self.ball.is_hit_surface(self.surface):
            self.ball.is_moving_up = True
            play_beep()

        if self.ball.visible:
            new_pos_x = (self.ball.current_position[0] + Constants.BALL_MOVEMENT_STEP) \
                if self.ball.is_moving_right else (self.ball.current_position[0] - Constants.BALL_MOVEMENT_STEP)
            new_pos_y = (self.ball.current_position[1] - Constants.BALL_MOVEMENT_STEP) if self.ball.is_moving_up \
                else (self.ball.current_position[1] + Constants.BALL_MOVEMENT_STEP)

            self.ball.current_position = (new_pos_x, new_pos_y)
            self.draw_new_ball()

    def draw_block(self, block: Block):
        row, col = block.position_in_board[0], block.position_in_board[1]
        block_x = int(col / (self.blocks_board.size[1] + 1) * self.display_width) - int(block.length / 2)
        block_y = int(Constants.BLOCK_VERTICAL_COEFFICIENT * (row / (self.blocks_board.size[0] + 1))
                      * self.display_height) + Constants.BLOCK_VERTICAL_MARGIN
        block.current_position = (block_x, block_y)
        block.visible = True
        for _ in range(block.length):
            self.drawer.draw(block)

    def blend(self, frame: ndarray):
        self.drawer.blend(frame)

    def get_drawer_output(self) -> ndarray:
        return self.drawer.output

    def adjust_winning_status(self):
        if not list(enumerate(filter(lambda block: block.alive, chain.from_iterable(self.blocks_board.blocks_list)))):
            self.is_winner = True
            self.ball.visible = False

    def toggle_block_visibility(self, block: Block):
        if block.visible:
            self.clear_block(block)
        else:
            self.draw_block(block)

    def draw_surface(self):
        self.drawer.draw(self.surface)

    def is_visible_player(self) -> bool:
        return self.player.is_visible

    def is_playing(self) -> bool:
        return self.is_winner is None
