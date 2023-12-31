
import gatt

from argparse import ArgumentParser


class AnyDevice(gatt.Device):
    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))
        if device.alias()=="Long name works now":
            return device.mac_address
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))


# arg_parser = ArgumentParser(description="GATT Connect Demo")
# arg_parser.add_argument('mac_address', help="MAC address of device to connect")
# args = arg_parser.parse_args()

print("Connecting...")

manager = gatt.DeviceManager(adapter_name='hci0')

device = AnyDevice(manager=manager, mac_address="A0:B7:65:49:F8:52")
device.connect()

manager.run()