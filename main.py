from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from http_client import HTTP_Client
from mqtt_client import MQTT_Client
from camera import Camera
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data")
async def root():
    client = HTTP_Client()
    return client.get()


@app.websocket("/mqtt")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    def on_message():
        asyncio.run(websocket.send_text(""))

    mqtt = MQTT_Client(on_message)
    mqtt.run()

    try:
        while True:
            data = await websocket.receive_text()
    except Exception as e:
        pass
    finally:
        pass


FACE = 100000


@app.websocket("/face")
async def face(websocket: WebSocket):
    await websocket.accept()
    camera = None
    try:
        camera = Camera()
        while True:
            image = camera.capture_image()
            results = camera.predict_face(image)
            if results.face_count != 0:
                max_face = max(results.faces, key=lambda x: x.w * x.h)
                if max_face.w * max_face.h > FACE:
                    await websocket.send_json(results.model_dump())
            await asyncio.sleep(0.1)
    except Exception as e:
        pass
    finally:
        if camera:
            del camera
    return
