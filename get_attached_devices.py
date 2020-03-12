import json
from operator import itemgetter
import re
from subprocess import Popen, PIPE

"""
Extract device serial numbers from "adb devices" command, so that they can be specified
in ADB commands (for when multiple devices are attached).
"""


def get_attached_devices(devices):
    # TODO: Use this function in one which copies a specified file to
    #       a specified folder on a specified device.

    adb_fn = "AdbListDevicesLong.bat"
    adb_file = open(adb_fn, "w")
    adb_exe = '"C:\\Program Files (x86)\\AndroidTools\\adb.exe"'
    adb_file.write(adb_exe + " devices -l" + "\n\n")
    #   "adb devices" lists the serial numbers of devices attached/connected via USB
    #   "adb devices -l" adds the following additional information:
    #       device product  (e.g. "angler", for my "Huawei Nexus 6P")
    #       model           (e.g. "Nexus_6P")
    #       device          (e.g. "angler")
    #       transport_id    (e.g. "2")
    adb_file.close()

    p = Popen([adb_fn], stdout=PIPE, stderr=PIPE, universal_newlines=True,)

    list_of_devices, errors = p.communicate()

    # According to "adb --help", options to ADB commands include:
    # 	-t ID			Use device with the given transport id
    # 	-s SERIAL		Use device with the given serial number

    transport_ids = {}
    serial_numbers = {}

    for device in devices:
        pattern = (
            r"model:" + devices[device] + r" device\:[A-Za-z0-9_]+ transport_id\:(\d)"
        )
        match = re.search(pattern, list_of_devices)
        if match:
            transport_ids[device] = match.group(1)
        pattern = r"([A-Za-z0-9]+)[ ]+device product\:.+model:" + devices[device]
        match = re.search(pattern, list_of_devices)
        if match:
            serial_numbers[device] = match.group(1)

    print("\nDevices attached (via USB), with their transport IDs:")
    if transport_ids:
        print(f"{json.dumps(transport_ids, indent=4)}")
    else:
        print("None")

    print("\nDevices attached (via USB), with their serial numbers:")
    if serial_numbers:
        print(f"{json.dumps(serial_numbers, indent=4)}")
    else:
        print("None")

    if errors:
        print(f"\nerrors:\n{errors}")

    return transport_ids


def main():
    my_devices = {  # Common name for the device: what "ADB devices" lists as "model"
        "Samsung Galaxy S3": "SPH_L710",
        "Huawei Nexus 6P": "Nexus_6P",
        "Motorola Droid RAZR M": "XT907",
    }
    attached_devices = get_attached_devices(my_devices)
    # input("\nPress any key to continue ")
    #   Use this if not running from within VSCode

    print("\nDevices attached (via USB), ordered by their transport IDs:")
    if attached_devices:
        # On StackOverflow, see:
        #   questions/613183/how-do-i-sort-a-dictionary-by-value/613207#613207
        # for attached_device in sorted(attached_devices, key=attached_devices.get):
        #     print(f"\t{attached_devices[attached_device]}: {attached_device}")
        for attached_device in sorted(attached_devices.items(), key=itemgetter(1)):
            print(f"\t{attached_device}")
    else:
        print("None")


if __name__ == "__main__":
    main()
