from picamera2 import Picamera2
import cv2
import numpy as np


class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
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


if __name__ == "__main__":
    camera = Camera()
    camera.capture_image()
