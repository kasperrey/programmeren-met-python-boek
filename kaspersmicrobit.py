from bleak import *
import time
import asyncio
from threading import Thread

MICROBIT_DEVICE_INFORMATION = '0000180a-0000-1000-8000-00805f9b34fb'
MICROBIT_EVENT_SERVICE = 'e95d93af-251d-470a-a062-fa1922dfa9a8'
MICROBIT_BUTTON_SERVICE = 'e95d9882-251d-470a-a062-fa1922dfa9a8'
MICROBIT_BUTTON_A = 'e95dda90-251d-470a-a062-fa1922dfa9a8'
MICROBIT_BUTTON_B = 'e95dda91-251d-470a-a062-fa1922dfa9a8'

BLUETOOTH_MICROBIT_OUD = '54:54:75:72:75:9E'
BLUETOOTH_MICROBIT_NIEUW = 'E3:7E:99:0D:C1:BA'

class ThreadEventLoop():
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        Thread(target=ThreadEventLoop._start_background_loop, args=(self.loop,), daemon=True).start()

    def _start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def run_async(self, coroutine):
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop)
        
class BluetoothEventLoop():
    _single_thread = ThreadEventLoop()

    def single_thread():
        return BluetoothEventLoop._single_thread;


class KaspersMicrobit():
    
    def __init__(self, address, loop=BluetoothEventLoop.single_thread()):
        self.loop = loop
        self.client = BleakClient(address)

    def connect(self):
        self.loop.run_async(self.client.connect()).result()
        print("connected")

    def disconnect(self):
        self.loop.run_async(self.client.disconnect()).result()
        print("disconnected")

    def notify(self, characteristic, callback):
        self.loop.run_async(self.client.start_notify(characteristic, callback)).result()
        print("notify")
