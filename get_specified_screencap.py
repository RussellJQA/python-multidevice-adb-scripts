from get_attached_devices import get_attached_devices
from get_screencaps import adb_screencap

# TODO: Parameterize this so that it can be called from the command line with a device
#       and it will get a screenshot from that device (if it's attached
#       [otherwise, it will give an error]).


def get_specified_screencap(device):
    attached_devices = get_attached_devices({f"{device}": "Nexus_6P"})
    if attached_devices:
        attached_device = attached_devices[device]
        serial_no = attached_device.serial_no
        transport_id = attached_device.transport_id
        print(f"\nGetting a screenshot for {device}: (serial_no={serial_no}, id={transport_id}).")
        adb_screencap(serial_no=f"{serial_no}")


def main():
    get_specified_screencap("Huawei Nexus 6P")
    input("\nPress any key to continue: ")


if __name__ == "__main__":
    main()
