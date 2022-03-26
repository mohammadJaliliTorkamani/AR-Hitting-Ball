import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def detect_gesture(self, cv_img):
        imgRGB = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        _cx, _cy = -1, -1
        points_status = {}

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = cv_img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    points_status[id] = (cx, cy)

        if 0 in points_status:
            return True, points_status[0]
        return False, (-1, -1)
