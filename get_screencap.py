import datetime
import os.path
import subprocess

from get_attached_devices import get_attached_devices


def adb_screencap(serial_no=None, id=None, adb_path=None):

    adb_exe = "adb" if adb_path is None else os.path.join(adb_path, "adb.exe")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    android_png_fn = "sdcard/" + timestamp + "-screenshot.png"
    win_png_fn = '"%UserProfile%\\Desktop\\' + timestamp + '-screenshot.png"'

    param = ""
    if serial_no is not None:
        param = f"-s {serial_no}"
    elif id is not None:
        param = f"-t {id}"

    adb_fn = os.path.join("batch", f"{timestamp}.bat")
    with open(adb_fn, "w") as adb_file:

        adb_file.write(f'"{adb_exe}" {param} shell screencap -p {android_png_fn}\n')
        adb_file.write(f'"{adb_exe}" {param} pull -a {android_png_fn} {win_png_fn}\n')
        adb_file.write(f'"{adb_exe}" {param} shell rm {android_png_fn}\n')

    adb_screencap_output = subprocess.check_output([adb_fn]).decode()

    return adb_screencap_output


def get_screencap(my_devices):

    attached_devices = get_attached_devices(my_devices)
    num_attached_devices = len(attached_devices)

    if num_attached_devices:
        print(f"\nThere are {num_attached_devices} device(s) attached:")
        for count, device in enumerate(attached_devices.items(), start=1):
            serial_no = device[1].serial_no
            id = device[1].id
            print(f"\tDevice #{count}: {device[0]}: (serial_no={serial_no}, id={id})")
        if num_attached_devices == 1:  # Exactly 1 device attached
            print(f"\nGetting a screenshot.")
            adb_screencap_output = adb_screencap()
            print(adb_screencap_output)
        elif num_attached_devices > 1:  # More than 1 device attached
            device_num = input(
                "\nWhich device do you want to take a screenshot of? "
                "Please enter its device #: "
            )
            (device_key, device) = list(attached_devices.items())[int(device_num) - 1]
            print(f"\nGetting a screenshot for device #{device_num}: {device_key}:")
            print(f"\t(serial_no={device.serial_no}, id={device.id}).")
            adb_screencap_output = adb_screencap(serial_no=f"{device.serial_no}")
            print(adb_screencap_output)
    else:
        print("ERROR: No devices are attached!")


def get_screencaps(my_devices):

    done = False
    while not done:
        get_screencap(my_devices)
        response = input(
            '\nPress "r" to repeat (get another screenshot), or any other key to quit: '
        ).lower()
        done = response != "r"


def main():

    my_devices = {
        "Samsung Galaxy S3": "SPH_L710",
        "Huawei Nexus 6P": "Nexus_6P",
        "Motorola Droid RAZR M": "XT907",
    }
    get_screencaps(my_devices)


if __name__ == "__main__":
    main()
