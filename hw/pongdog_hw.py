
import evdev
from evdev import categorize, ecodes
from select import select
import time
from gpiozero import LED

p1_led = LED(18)
p2_led = LED(4)

class Device():
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
                select([device], [], [], 2)
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
                    print("Timeout!")
                    return str(0)
        except:
            # catch all exceptions to be able release the device
            device.ungrab()
            print('Quitting.')


def read_cards():

    while True:
        p1_led.off()
        p2_led.off()
        print("Player 1, please scan card")
        player1 = Device.run()

        print("Player 1, card ID:" + player1)
        p1_led.on()
        # light up lys #1 
        print("Player 2, please scan card")
        player2 = Device.run()
        
        print("Player 2, card ID:" + player2)
        if player1 == player2:
            p1_led.off()
            p2_led.off()
            print("Error! Same card detected!")
            time.sleep(1)
            # blink rødt lys
        else:
            break
    print("Two unique cards detected wahoo")
    p2_led.on()
    time.sleep(1)
    p1_led.off()
    p2_led.off()
    p1_led.blink(0.1,0.1,10)
    p2_led.blink(0.1,0.1,10)
    while True:
        pass
    # light up lys #2



def initiate_game(abort):
    print("HAWA")

read_cards()