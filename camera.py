from picamera2 import Picamera2
import cv2
import numpy as np
from json import loads
from websockets.sync.client import connect
from time import sleep
from adptars import FaceDetectionResult, Face

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def predict_face(img: np.ndarray):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    result = FaceDetectionResult(
        face_count=len(faces),
        faces=[Face(x=int(x), y=int(y), w=int(w), h=int(h)) for (x, y, w, h) in faces],
    )
    return result




if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        result = predict_face(frame)
        if result.face_count == 0:
            pass
        else:
            cv2.rectangle(
                frame,
                (result.faces[0].x, result.faces[0].y),
                (
                    result.faces[0].x + result.faces[0].w,
                    result.faces[0].y + result.faces[0].h,
                ),
                (255, 0, 0),
                2,
            )
            print(result.faces[0].w * result.faces[0].h)
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
    cv2.destroyAllWindows()
