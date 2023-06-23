import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import time
esp_addr="4FAFC201-1FB5-459E-8FCC-C5C9331914B"
esp_name="Long name works now"
esp_test_UUID="42c02b73-0b43-492e-8941-91a547a180f0"
async def main():
    devices = await BleakScanner.find_device_by_name(esp_name)
    print(devices.name)
    async with BleakClient(devices) as client:
            #print(client.address)
        data= await client.read_gatt_char(esp_test_UUID)
        print(int.from_bytes(data,"little"))
       #await client.disconnect()
    

while 1:
    asyncio.run(main())
    time.sleep(30)