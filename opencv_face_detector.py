from fastapi import FastAPI, WebSocket
import cv2
import numpy as np
import starlette
from adptars import FaceDetectionResult, Face

app = FastAPI()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            result = FaceDetectionResult(
                face_count=len(faces),
                faces=[
                    Face(x=int(x), y=int(y), w=int(w), h=int(h))
                    for (x, y, w, h) in faces
                ],
            )
            await websocket.send_json(result.model_dump())
    except starlette.websockets.WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # http://localhost:8000/ws
