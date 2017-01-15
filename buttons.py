import time
from threading import Thread

import RPi.GPIO as GPIO

from util import thread_it


class Button:
    down = False

    def __init__(self, callback, current_state=False):
        self.callback = callback
        self.current_state = current_state


class Buttons:
    pins = {}

    @staticmethod
    def watch_button(pin_number, callback2, current_state=False):
        Buttons.pins[pin_number] = Button(callback2, current_state)

    @staticmethod
    def check_buttons():
        while True:
            for pin in Buttons.pins.keys():
                button = Buttons.pins[pin]
                if not GPIO.input(pin):
                    if not button.down:
                        print("pin change", pin)
                        button.current_state = not button.current_state;
                        button.callback(button.current_state)
                        button.down = True
                else:
                    button.down = False

            time.sleep(.1)


thread_it(lambda: Buttons.check_buttons)
print("IO thread inited")
