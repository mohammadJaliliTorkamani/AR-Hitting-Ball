class Player:
    def __init__(self):
        self.position = (0, 0)
        self.hand_status = 0 # Fist : 0, Open Hand : 1
        self.visible = False

    def detect_gesture(self):
        pass