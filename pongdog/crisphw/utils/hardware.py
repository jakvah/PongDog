from gpiozero import LED, Button
import signal

p1_led = LED(16)
p2_led = LED(26)
p1_button = Button(20)
p2_button = Button(19)

def handleSignal(num, stack):
    return 0

signal.signal(signal.SIGUSR1, handleSignal)