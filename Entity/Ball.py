from dataclasses import dataclass

from Entity.Drawable import Drawable
from Utils import Constants


@dataclass
class Ball(Drawable):
    is_moving_up: bool = True
    is_moving_right: bool = True

    def _is_horizontally_on_block(self, block):
        return block.current_position[0] <= self.current_position[0] <= block.get_end_position_in_frame()[0]

    def _is_vertically_on_block(self, block):
        block_top_side_with_ball_margin = block.current_position[1] - 2 * Constants.PIXEL_DIMENSION
        block_bottom_side_with_ball_margin = block.current_position[1] + 2 * Constants.PIXEL_DIMENSION

        return block_top_side_with_ball_margin <= self.current_position[1] <= block_bottom_side_with_ball_margin

    def hit_block(self, block):
        return self._is_horizontally_on_block(block) and self._is_vertically_on_block(block)
