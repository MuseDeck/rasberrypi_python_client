import cv2
import numpy as np
from adptars import FaceDetectionResult, Face


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        result = FaceDetectionResult(
            face_count=len(faces),
            faces=[
                Face(x=int(x), y=int(y), w=int(w), h=int(h)) for (x, y, w, h) in faces
            ],
        )
        return result


if __name__ == "__main__":
    detector = FaceDetector()
    img = cv2.imread("./sample1.jpg")
    result = detector.detect(img)
    print(result)
