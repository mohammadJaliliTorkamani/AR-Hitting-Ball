import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self._hands = mp.solutions.hands.Hands()

    def detect_gesture(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(img_rgb)
        _cx, _cy = -1, -1
        points_status = {}

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    points_status[id] = (cx, cy)

        if 0 in points_status:
            return True, points_status[0]
        return False, (-1, -1)
