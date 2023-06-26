import asyncio
import os
import sys,time
from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

ESP_NAME="UART"

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


async def uart_terminal(esp_name):


    

    device = await BleakScanner.find_device_by_name(esp_name)
    print(device.name)

    if device == None:
        print("no matching device found, you may need to edit match_nus_uuid().")
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()
        

        sys.exit(1)
        

    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        print("received:", data)


   
    #async with BleakClient(device, disconnected_callback=handle_disconnect,timeout=100000000) as client:
    #async with BleakClient(device) as client:
        #print("connected")
    client = BleakClient(device,handle_disconnect)
    print('Connecting...')
    await client.connect()
    if not client.is_connected:
        print('Failed to connect')
    else:
        #client.set_disconnected_callback(handle_disconnect)
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        print("Connected, start typing and press ENTER")

        loop = asyncio.get_running_loop()
        nus = client.services.get_service(UART_SERVICE_UUID)
        rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

                # data will be empty on EOF (e.g. CTRL+D on *nix)
            if not data:
                break

            for s in sliced(data, rx_char.max_write_without_response_size):
                await client.write_gatt_char(rx_char, s)

            print("sent:", data)


if __name__ == "__main__":  
        while True:
            
            try:
                asyncio.run(uart_terminal(ESP_NAME))
            except :
                # task is cancelled on disconnect, so we ignore this error
                pass
            time.sleep(3)