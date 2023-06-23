import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import time

#add the name of the device here
esp_name="Long name works now"
#add the characteristic UUID here
esp_test_UUID="42c02b73-0b43-492e-8941-91a547a180f0"


async def run(name):
    print("Finding device now\n")
    devices = await BleakScanner.find_device_by_name(name)
    print(devices.name)
    if devices != None:
        print("Connecting")
        async with BleakClient(devices) as client:
            #successfully connected 
            #add your code here
            data= await client.read_gatt_char(esp_test_UUID)
            print(int.from_bytes(data,"little"))
       #await client.disconnect()
    else:
        print("ERROR: No device was found!\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(esp_name))
time.sleep(5)
loop.run_until_complete(run(esp_name))