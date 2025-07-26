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


class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.picam2.start()

    def nv12_to_rgb(self, nv12_array, width, height):
        y_plane = nv12_array[: width * height].reshape((height, width))
        uv_plane = nv12_array[width * height :].reshape((height // 2, width // 2, 2))
        uv_plane = cv2.resize(uv_plane, (width, height), interpolation=cv2.INTER_LINEAR)
        yuv = np.dstack((y_plane, uv_plane[:, :, 0], uv_plane[:, :, 1]))
        rgb = cv2.cvtColor(yuv.astype(np.uint8), cv2.COLOR_YUV2RGB)
        return rgb

    def capture_image(self) -> np.ndarray:
        image = self.picam2.capture_buffer("main")
        config = self.picam2.camera_config
        width, height = config["main"]["size"]
        image_array = np.frombuffer(image, dtype=np.uint8)
        image_rgb = self.nv12_to_rgb(image_array, width, height)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        return image_bgr

    def predict_face(self, img: np.ndarray):
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
    camera = Camera()
    while True:
        result = camera.predict_face(camera.capture_image())
        if result.face_count > 0:
            for face in result.faces:
                print(face.w * face.h, end="\t")
            print()
        sleep(0.1)
