from Utils.HandDetector import HandDetector


class Player:
    def __init__(self):
        self.current_position = (0, 0)
        self.last_position = (0, 0)
        self.is_visible = False
        self.detector = HandDetector()

    def detect_gesture(self, frame):
        return self.detector.detect_gesture(frame)