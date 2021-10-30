
import evdev
from evdev import categorize, ecodes
from select import select
import time
from gpiozero import LED
import requests

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
                select([device], [], [], 5)
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


#reads cards and makes sure that the cards exists in the database. Also handles duplicate cards
def read_cards():
    while True:
        p1_led.off()
        p2_led.off()

        print("Player 1, please scan card")
        player1 = Device.run()
        player1 = "20203020"
        if player1 == "0":
            continue # card reader timed out
        print("Player 1, card ID:" + player1)
        if check_card(player1) != "200":
            #play_denied()
            continue
        p1_led.on()

        print("Player 2, please scan card")
        player2 = Device.run()
        if player2 == "0":
            continue # card reader timed out
        print("Player 2, card ID:" + player2)

        if player1 == player2:
            p1_led.off()
            p2_led.off()
            print("Error! Same card detected!")
            time.sleep(1)
            # blink rødt lys
        else:
            #if checkCard(player2) != riktig svar
                #play_denied()
                #continue
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

#checks if user registered on PongDog. Returns True if card is registered, false if not or error occurs.
def check_card(card_id):
    url = f"https://jakvah.pythonanywhere.com/get_card_status/{card_id}"
    r = requests.get(url)
    print(r.text)
    if r.text == "200":
        print(r.text)
        return True
    elif r.text == "300":
        print(r.text)
        return False
    else:
        return False

#check if a match is running. Returns 0 if available, 1 if busy, 2 if error.
def check_game_state():
    url = f"https://jakvah.pythonanywhere.com/get_match_status"
    r = requests.get(url)
    print(r.text)
    if r.text == "200":
        return 1
    elif r.text == "300":
        return 0
    else:
        return 2

# Resets the backend. Returns True if reset successful.
def reset_match():
    url = f"https://jakvah.pythonanywhere.com/reset_match_status/pongdg4life"
    r = requests.post(url)
    print(r.text)
    if r.text == "200":
        return True
    else:
        return False


def initiate_game():
    p1_score = 0
    p2_score = 0

    print("HAWA")

read_cards()