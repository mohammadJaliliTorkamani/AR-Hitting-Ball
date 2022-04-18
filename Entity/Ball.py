from dataclasses import dataclass

from Entity.Block import Block
from Entity.Drawable import Drawable
from Entity.Surface import Surface
from Utils import Constants


@dataclass
class Ball(Drawable):
    is_moving_up: bool = True
    is_moving_right: bool = True

    def _is_horizontally_on_block(self, block: Block) -> bool:
        return block.current_position[0] <= self.current_position[0] <= block.get_end_position_in_frame()[0]

    def _is_horizontally_on_surface(self, surface: Surface) -> bool:
        return surface.current_position[0] <= self.current_position[0] <= surface.get_end_x()

    def _is_vertically_on_block(self, block: Block) -> bool:
        block_top_side_with_ball_margin = block.current_position[1] - 2 * Constants.PIXEL_DIMENSION
        block_bottom_side_with_ball_margin = block.current_position[1] + 2 * Constants.PIXEL_DIMENSION

        return block_top_side_with_ball_margin <= self.current_position[1] <= block_bottom_side_with_ball_margin

    def _is_vertically_on_surface(self, surface: Surface) -> bool:
        ball_bottom_side = self.current_position[1] + Constants.PIXEL_DIMENSION

        return (surface.current_position[1] - Constants.PIXEL_DIMENSION) \
               <= ball_bottom_side <= \
               (surface.current_position[1] + Constants.PIXEL_DIMENSION)

    def is_hit_block(self, block: Block) -> bool:
        return self._is_horizontally_on_block(block) and self._is_vertically_on_block(block)

    def is_hit_surface(self, surface: Surface) -> bool:
        return self._is_horizontally_on_surface(surface) and self._is_vertically_on_surface(surface)

    def is_horizontally_aligned(self, display_width: int) -> bool:
        return (self.current_position[0] + Constants.PIXEL_DIMENSION <= display_width) \
               and (self.current_position[0] - Constants.PIXEL_DIMENSION >= 0)

    def toggle_moving_right(self):
        self.is_moving_right = not self.is_moving_right

    def toggle_moving_up(self):
        self.is_moving_up = not self.is_moving_up

    def is_vertically_top_aligned(self) -> bool:
        return self.current_position[1] >= 0

    def is_vertically_in_range(self, display_height) -> bool:
        return self.current_position[1] <= display_height
