from ultralytics import YOLO
import numpy as np
import zmq


class FaceDetector:
    def __init__(self):
        self.model = YOLO("./weights/yolov12n-face.pt")

    def predict(self, image: np.ndarray | str):
        results = self.model(image)
        return results[0].boxes.xywh.cpu().numpy()


if __name__ == "__main__":
    detector = FaceDetector()
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        image = socket.recv_pyobj()
        assert isinstance(image, np.ndarray), "Received image is not a numpy array"
        results = detector.predict(image)
        socket.send_pyobj(results)
