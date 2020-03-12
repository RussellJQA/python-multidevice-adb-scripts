from operator import itemgetter
import re
from subprocess import Popen, PIPE

"""
For when multiple Android devices are attached/connected via USB:
    Get a dictionary of the devices attached/connected, indexed by their transport IDs.
    Those transport IDs can then be specified as options to ADB commands.
"""


def get_attached_devices(devices):

    adb_fn = "AdbListDevicesLong.bat"
    with open(adb_fn, "w") as adb_file:
        adb_exe = '"C:\\Program Files (x86)\\AndroidTools\\adb.exe"'
        adb_file.write(adb_exe + " devices -l" + "\n\n")

    #   "adb devices" lists the serial numbers of devices attached/connected via USB
    #   "adb devices -l" adds the following additional information:
    #       device product  (e.g. "angler", for my "Huawei Nexus 6P")
    #       model           (e.g. "Nexus_6P")
    #       device          (e.g. "angler")
    #       transport_id    (e.g. "4")
    #
    #   According to "adb --help", options to ADB commands include:
    # 	    -t ID			Use device with the given transport id
    # 	    -s SERIAL		Use device with the given serial number

    p = Popen([adb_fn], stdout=PIPE, stderr=PIPE, universal_newlines=True,)

    list_of_devices, errors = p.communicate()

    attached_devices = {}
    #   devices attached/connected (via USB), indexed by tranport IDs

    for device in devices:
        pattern = (
            r"model:" + devices[device] + r" device\:[A-Za-z0-9_]+ transport_id\:(\d)"
        )
        match = re.search(pattern, list_of_devices)
        if match:
            attached_devices[match.group(1)] = device

    if errors:
        print(f"\nerrors:\n{errors}")

    return attached_devices


def main():
    my_devices = {
        # key: common name for the device
        # value: what "ADB devices" lists as "model"
        "Samsung Galaxy S3": "SPH_L710",
        "Huawei Nexus 6P": "Nexus_6P",
        "Motorola Droid RAZR M": "XT907",
    }
    attached_devices = get_attached_devices(my_devices)
    # TODO: If possible, programatically determine whether to include the following:
    # input("\nPress any key to continue ")
    #   Use this if not running from within VSCode

    print("\nDevices attached/connected (via USB), indexed by their transport IDs:")
    if attached_devices:
        for (transport_id, attached_device) in sorted(attached_devices.items()):
            print(f"\t{transport_id}: {attached_device}")
    else:
        print("None")


if __name__ == "__main__":
    main()
