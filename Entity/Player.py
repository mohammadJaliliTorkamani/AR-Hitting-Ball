class Player:
    def __init__(self):
        self.position = (0, 0)
        self.hand_status = 0  # None-open : 0, Open Hand : 1
        self.is_visible = False
