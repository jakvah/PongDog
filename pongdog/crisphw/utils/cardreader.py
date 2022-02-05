import evdev
from evdev import categorize, ecodes
from select import select

class Cardreader():
    name = 'Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader'

    @classmethod
    def list(cls, show_all=False):
        # list the available devices
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if show_all:
            for device in devices:
                print("event: " + device.fn, "name: " + device.name, "hardware: " + device.phys)
        return devices

    @classmethod
    def connect(cls):
        # connect to device if available
        try:
            device = [dev for dev in cls.list() if cls.name in dev.name][0]
            device = evdev.InputDevice(device.path)
            return device
        except IndexError:
            print("Device not found.\n - Check if it is properly connected. \n - Check permission of /dev/input/ (see README.md)")
            exit()

    @classmethod
    def run(cls):
        device = cls.connect()
        container = []
        try:
            device.grab()
            # bind the device to the script
            #print("RFID scanner is ready....")
            #print("Press Control + c to quit.")
            while True:
                select([device], [], [], 20)
                try:
                    for event in device.read():
                            # enter into an endeless read-loop
                            if event.type == ecodes.EV_KEY and event.value == 1:
                                digit = evdev.ecodes.KEY[event.code]
                                if digit == 'KEY_ENTER':
                                    # create and dump the tag
                                    tag = "".join(i.strip('KEY_') for i in container)
                                    return tag
                                    print(tag)
                                    container = []
                                else:
                                    container.append(digit)
                except BlockingIOError:
                    print("Card-reader timed out.")
                    return str(0)
        except:
            # catch all exceptions to be able release the device
            device.ungrab()
            print('Quitting.')