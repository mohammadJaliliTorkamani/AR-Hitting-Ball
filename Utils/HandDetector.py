import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def detect_gesture(self, cv_img):
        results = self.hands.process(cv_img)
        points_status = {}
        if results.multi_hand_landmarks:
            for handLMS in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(handLMS.landmark):
                    h, w, c = cv_img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    points_status[id] = (cx, cy)
                if (points_status[0][1] > points_status[20][1] > points_status[8][1]) and (
                        points_status[20][0] > points_status[8][0] > points_status[4][0]) and (
                        points_status[4][1] > points_status[20][1] > points_status[16][1]):  # open hand detected
                    return True, points_status[9], 1
                else:
                    return True, (points_status[7][0], points_status[7][1]), 0

        return False, (-1, -1), 1