from bluepy.btle import Peripheral, UUID, DefaultDelegate
import time
import json
import time


UART_SERVICE_UUID = UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
TX_CHAR_UUID = UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
RX_CHAR_UUID = UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e")


class NotificationDelegate(DefaultDelegate):
    def __init__(self, device, tx_char):
        DefaultDelegate.__init__(self)
        self.device = device
        self.tx_characteristic = tx_char
        self.received_data = b""  # Variable to accumulate received data

    def handleNotification(self, cHandle, data):
        try:
            self.received_data += data  # Accumulate received data
            # print("Rx len: ", len(data), data)

            # Check if the complete data is received
            if self.is_complete_data_received():
                hex_values = " ".join("{:02x}".format(byte)
                                      for byte in self.received_data)
                print("Received data (Length: {}):".format(
                    len(self.received_data)))
                # print("Hex values:", hex_values)
                # client.publish(MQTT_TOPIC, self.received_data)
                # self.send_data(b"ACK\n")

                # Reset received_data for the next set of data
                self.received_data = b""

        except UnicodeDecodeError as e:
            print("Error:", e)

    def send_data(self, data):
        try:
            self.tx_characteristic.write(data)
        except Exception as e:
            print("Failed to send data:", str(e))

    def is_complete_data_received(self):
        return b"\n" in self.received_data


def connect_to_device(address):
    isConnected = False
    while True:
        try:
            # Connect to the device
            print("Connecting to device:", address)
            device = Peripheral(address)
            print("Connected!")
            isConnected = True
            # Request maximum MTU size
            mtu_size = 512
            device.setMTU(mtu_size)
            print("Requested MTU size:", mtu_size)

            # Discover UART service
            uart_service = device.getServiceByUUID(UART_SERVICE_UUID)

            # Discover TX and RX characteristics
            tx_characteristic = uart_service.getCharacteristics(TX_CHAR_UUID)[
                0]
            rx_characteristic = uart_service.getCharacteristics(RX_CHAR_UUID)[
                0]

            # Enable notifications on the RX characteristic
            device.writeCharacteristic(
                rx_characteristic.getHandle() + 1, b"\x01\x00", withResponse=True)

            # Set the notification delegate
            notification_delegate = NotificationDelegate(
                device, tx_characteristic)
            device.withDelegate(notification_delegate)

            # Enter an infinite loop to continuously print incoming data
            while True:
                if device.waitForNotifications(1.0):
                    continue

        except Exception as e:
            print("Connection failed:", str(e))
            print("Reconnecting...")
            if isConnected:
                device.disconnect()
            else:
                print("Never connected, try next...")
                time.sleep(5)  # Wait for 1 second before reconnecting
            time.sleep(3)  # Wait for 1 second before reconnecting
            continue


def process_matching_devices():
    # mqtt_connect()
    # connect_to_device("94:e6:86:92:da:42")
    connect_to_device("84:cc:a8:2e:87:9e")


# Start processing the matching devices
process_matching_devices()
# mqtt_connect()
