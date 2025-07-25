import os
import sys
import asyncio
from dotenv import load_dotenv
from time import sleep

load_dotenv()
SENSOR_SDK_PATH = os.getenv("SENSOR_SDK_PATH")
sys.path.append(SENSOR_SDK_PATH)

from DFRobot_PAJ7620U2 import *

paj = DFRobot_PAJ7620U2(1)


class GestureSensor:
    def __init__(self, callback):
        self.callback = callback
        while paj.begin() != 0:
            sleep(0.5)
        paj.set_gesture_highrate(True)

    async def run(self):
        while True:
            gesture = paj.get_gesture()
            if gesture == paj.GESTURE_NONE:
                continue
            await self.callback(paj.gesture_description(gesture))
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    sensor = GestureSensor(lambda x: print(x))
