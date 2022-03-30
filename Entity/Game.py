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
                block.position_in_frame = (
                    int(col / (self.blocks_board.size[1] + 1) * self.display_width) - int(block.length / 2),
                    int(0.4 * (row / (self.blocks_board.size[0] + 1)) * self.display_height) + 10)
                self.draw_block(block)

    def detect_gesture(self, cv_img):
        visible, position = self.detector.detect_gesture(cv_img)
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
            for i in range(self.surface.length):
                self.drawer.clear((self.surface.last_x + i, self.surface.y))

    def draw_surface(self):
        for i in range(self.surface.length):
            self.drawer.draw((self.surface.current_x + i, self.surface.y), 0)

    def clear_last_ball(self):
        self.drawer.clear(self.ball.last_position)

    def draw_ball(self):
        self.drawer.draw(self.ball.current_position, 1)

    def remove_block(self, block_length, block_position):
        for k in range(block_length):
            block_x = int(block_position[1] / (
                    self.blocks_board.size[1] + 1) * self.display_width) + k - int(block_length / 2)
            block_y = int(0.4 * (block_position[0] / (
                    self.blocks_board.size[0] + 1)) * self.display_height) + 10
            self.drawer.clear((block_x, block_y))

    def move_ball(self):
        if self.surface.current_x is None:
            return

        self.ball.last_position = self.ball.current_position

        ### BLOCK COLLISION STATE CHECK
        for block_row in self.blocks_board.blocks:
            for block in block_row:
                if block.alive:
                    if (block.position_in_frame[0] <= self.ball.current_position[0] <= block.position_in_frame[0]
                        + block.length) and (self.ball.current_position[1] == block.position_in_frame[1]):
                        self.ball.is_moving_up = not self.ball.is_moving_up
                        block.alive = False
                        self.remove_block(block.length, block.position)

        if (self.ball.current_position[0] == self.display_width) or (self.ball.current_position[0] == 0):
            self.ball.is_moving_right = not self.ball.is_moving_right

        elif self.ball.current_position[1] == 0:
            self.ball.is_moving_up = False

        elif self.ball.current_position[1] == self.display_height:
            print("You lose!")
            pass
        elif ((self.surface.current_x <= self.ball.current_position[0] <= (
                self.surface.current_x + self.surface.length))
              and ((self.ball.current_position[1] + 10) == self.surface.y)):
            self.ball.is_moving_up = True

        if self.ball.is_moving_right:
            new_pos_x = (self.ball.current_position[0] + 1)
        else:
            new_pos_x = (self.ball.current_position[0] - 1)

        if self.ball.is_moving_up:
            new_pos_y = (self.ball.current_position[1] - 1)
        else:
            new_pos_y = (self.ball.current_position[1] + 1)

        self.ball.current_position = (new_pos_x, new_pos_y)
        self.clear_last_ball()
        self.draw_ball()

    def draw_block(self, block):
        for k in range(block.length):
            self.drawer.draw((block.position_in_frame[0] + k, block.position_in_frame[1]), 2)
