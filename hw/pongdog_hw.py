
import evdev
from evdev import categorize, ecodes
from select import select
import time
from gpiozero import LED
import requests
import datetime

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

def get_timestamp():
    dato = str(datetime.datetime.now())
    date = dato.split(' ')[0]
    klokkeslett = dato.split(' ')[1]
    dog = klokkeslett.split('.')[0]
    fulltimestamp = date+'T'+dog
    return fulltimestamp

#reads cards and makes sure that the cards exists in the database. Also handles duplicate cards
def read_cards():
    while True:
        p1_led.off()
        p2_led.off()

        print("Player 1, please scan card")
        #player1 = Device.run()
        player1 = "128"
        if player1 == "0":
            continue # card reader timed out
        print("Player 1, card ID:" + player1)
        p1_led.blink(0.1,0.1,30)
        if not check_card(player1):
            #play_denied()
            continue
        p1_led.on()

        print("Player 2, please scan card")
        #player2 = Device.run()
        player2 = "224"
        if player2 == "0":
            continue # card reader timed out
        print("Player 2, card ID:" + player2)

        if player1 == player2: # same card inserted
            p1_led.off()
            p2_led.off()
            print("Error! Same card detected!")
            #play_denied()
            time.sleep(1)
            continue
        else:
            p2_led.blink(0.1,0.1,30)
            if not check_card(player2): # card does not exist
                #play_denied()
                continue #start over
            p2_led.on()
            break
    print("Two unique cards detected wahoo")
    return player1, player2
    
    # light up lys #2

#checks if user registered on PongDog. Returns True if card is registered, false if not or error occurs.
def check_card(card_id):
    url = f"https://jakvah.pythonanywhere.com/get_card_status/{card_id}"
    r = requests.get(url)
    if r.text == "200":
        return True
    elif r.text == "300":
        print(r.text)
        return False
    else:
        return False

#check if a match is running. Returns 1 if available, 0 if busy, 2 if error.
def get_match_status():
    url = f"https://jakvah.pythonanywhere.com/get_match_status"
    r = requests.get(url)
    print("get_match_status: "+ r.text)
    if r.text == "300":
        return 1
    elif r.text == "200":
        return 0
    else:
        return 2

# Resets the backend. Returns True if reset successful.
def reset_match():
    url = f"https://jakvah.pythonanywhere.com/reset_match_status/pongdg4life"
    r = requests.get(url)
    print("reset_match: "+r.text)
    if r.text == "200":
        return True
    else:
        return False

# Sends the player ID's and timestamp to backend. Returns true if succeeded.
def start_match(p1_id, p2_id):
    time_now = get_timestamp()
    url = f"https://jakvah.pythonanywhere.com/init_match/{p1_id}/{p2_id}/{time_now}"
    r = requests.post(url)
    print("start_match: "+r.text)
    if r.text == "200":
        return True
    else:
        return False


# checks that a game isn't running and sends p1 and p2 and timestamp to backend. Returns true if all good.
def initiate_game(player1, player2):
    if get_match_status() != 1:
        print("game currently underway!")
        return False
    if start_match(player1,player2):
        return True
    else:
        print("start_match(): Failed to start game")
        return False


while True: 
    p1, p2 = read_cards()
    initiate_game(p1, p2)
    #poll buttons