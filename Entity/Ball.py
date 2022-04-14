from Entity.Drawable import Drawable


class Ball(Drawable):
    def __init__(self, color=None, current_position=None, last_position=(0, 0)):
        super().__init__(color, current_position.current_position, last_position)
        self.is_moving_up = True
        self.is_moving_right = True
