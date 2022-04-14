from Entity.Drawable import Drawable


class Ball(Drawable):
    def __init__(self, color=None, current_position=(-1, -1), last_position=(-1, -1)):
        super().__init__(color, current_position, last_position)
        self.is_moving_up = True
        self.is_moving_right = True
