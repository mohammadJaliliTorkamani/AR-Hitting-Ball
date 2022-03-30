class Surface:
    _SURFACE_LENGTH = 70

    def __init__(self, y):
        self.length = Surface._SURFACE_LENGTH
        self.current_x = None
        self.last_x = None
        self.y = y
