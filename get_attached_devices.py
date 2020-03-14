import collections
import json
import os.path
import re
import subprocess

"""
For when multiple Android devices are attached/connected via USB:
    Get dictionary of the devices attached/connected, with a named tuple of their:
        serial number
        transport ID
    The serial numbers or transport IDs can then be specified as options to ADB
    commands.
    Although the transport IDs are simpler to specify, they can change.
"""

Device = collections.namedtuple("Device", "serial_no id")


def get_attached_devices(devices, adb_path=None):

    adb_fn = "AdbListDevicesLong.bat"
    with open(adb_fn, "w") as adb_file:

        adb_exe = "adb" if adb_path is None else os.path.join(adb_path, "adb.exe")
        adb_file.write(f'"{adb_exe}" devices -l\n\n')
        #   Need to include double quotation marks in what's written to adb_file.

    #   "adb devices" lists the serial numbers of devices attached/connected via USB
    #   "adb devices -l" adds the following additional information:
    #       device product  (e.g. "angler", for my "Huawei Nexus 6P")
    #       model           (e.g. "Nexus_6P")
    #       device          (e.g. "angler")
    #       transport_id    (e.g. "4")
    #
    #   According to "adb --help", options to ADB commands include:
    # 	    -t ID			Use device with the given transport ID
    # 	    -s SERIAL		Use device with the given serial number

    list_of_devices = subprocess.check_output([adb_fn]).decode()

    attached_devices = {}
    #   devices attached/connected (via USB), indexed by tranport IDs

    for device in devices:

        transport_id = None
        serial_number = None

        # Search for the device's serial number
        pattern = r"([A-Za-z0-9]+)[ ]+device product\:.+model:" + devices[device]
        match = re.search(pattern, list_of_devices)
        if match:
            serial_number = match.group(1)

            # Search for the device's transport ID
            pattern = (
                r"model:"
                + devices[device]
                + r" device\:[A-Za-z0-9_]+ transport_id\:(\d)"
            )
            match = re.search(pattern, list_of_devices)
            if match:
                transport_id = match.group(1)

        if transport_id is not None and serial_number is not None:
            attached_devices[device] = Device(serial_no=serial_number, id=transport_id)

    return attached_devices


def main():

    # TODO: Put this dictionary in a JSON file which can be referenced by any of these
    #       scripts.
    my_devices = {
        # key: common name for the device
        # value: what "ADB devices" lists as "model"
        "Samsung Galaxy S3": "SPH_L710",
        "Huawei Nexus 6P": "Nexus_6P",
        "Motorola Droid RAZR M": "XT907",
    }

    # NOTE to users: If your folder which contains ADB.exe is not in your path,
    #   then you need to specify its location simlar to how it's done below:
    # ADB_PATH = r"C:\ProgramData\chocolatey\lib\adb\tools\platform-tools"
    # attached_devices = get_attached_devices(my_devices, ADB_PATH)

    attached_devices = get_attached_devices(my_devices)
    count = len(attached_devices)

    print(f"\n{count} devices attached, with their serial numbers and transport IDs:")
    if count:
        for device in attached_devices.items():
            print(
                f"\t{device[0]}: (serial_no={device[1].serial_no}, id={device[1].id})"
            )
    else:
        print("None")

    input("\nPress any key to continue: ")


if __name__ == "__main__":
    main()
