from gpiozero import LED, Button
import signal

p1_led = LED(26)
p2_led = LED(16)
p1_button = Button(19)
p2_button = Button(20)


def p1_led_blink(on,off,n)
    p1_led.blink(on,off,n)