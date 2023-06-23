import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import time

#add the name of the device here
esp_name="Long name works now"
#add the characteristic UUID here
esp_test_UUID="42c02b73-0b43-492e-8941-91a547a180f0"


async def run(name):
    print("Finding device now")
    devices = await BleakScanner.find_device_by_name(name)
    print(devices.name)
    if devices != None:
        print("Connecting")
        async with BleakClient(devices) as client:
            #successfully connected 
            #add your code here
            client.mtu_size=512 #change mtu size
            data= await client.read_gatt_char(esp_test_UUID)
            rint(int.from_bytes(data,"little"))
            
        # except:
        #     print("Error")
       #await client.disconnect()
    else:
        print("ERROR: No device was found!")


#add your code here
loop = asyncio.get_event_loop()
while 1:
    loop.run_until_complete(run(esp_name))
    time.sleep(10)
    loop.run_until_complete(run(esp_name))