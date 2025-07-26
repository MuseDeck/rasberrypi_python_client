import cv2
import mediapipe as mp
import numpy as np


class Pen:
    def __init__(self, callback=lambda *x: print(x), distance_min=0.1):
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.callback = callback
        self.distance_min = distance_min

    def start(self):
        while True:
            success, img = self.cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)
            if not results.multi_hand_landmarks:
                continue
            for handLms in results.multi_hand_landmarks:
                target_finger1, target_finger2 = None, None
                for id, lm in enumerate(handLms.landmark):
                    if id == 4:
                        target_finger1 = np.array([lm.x, lm.y])
                    if id == 8:
                        target_finger2 = np.array([lm.x, lm.y])
                distance = np.linalg.norm(target_finger1 - target_finger2)
                self.callback(target_finger1, target_finger2)


if __name__ == "__main__":
    pen = Pen()
    pen.start()
