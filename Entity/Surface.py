from Utils import Constants


class Surface:
    def __init__(self, y):
        self.length = Constants.SURFACE_LENGTH
        self.current_x = None
        self.last_x = None
        self.y = y

    def get_end_x(self):
        if self.current_x is not None:
            return self.current_x + self.length
        return -1
