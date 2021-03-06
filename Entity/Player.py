from dataclasses import dataclass

from numpy import ndarray

from Utils.HandDetector import HandDetector


@dataclass
class Player:
    current_position: tuple = (0, 0)
    last_position: tuple = (0, 0)
    is_visible: bool = False
    detector: HandDetector = HandDetector()

    def detect_gesture(self, frame: ndarray) -> (bool, tuple):
        return self.detector.detect_gesture(frame)
