import time
from math import fabs

import RPi.GPIO as GPIO
from gpiozero import MCP3008

from nester import Nester
from buttons import Buttons
from chromecast import EZChromeCast
from ezhue import EZHue, HueColors
from irremote import IrRemote, Command
from util import thread_it


class DreamMachine:
    LIGHT_BUTTON_PIN = 21
    CHROMECAST_BUTTON_PIN = 16
    IR_PIN = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CHROMECAST_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __init__(self, cfg=None):
        self.nest = Nester(cfg)
        print("Starting the DreamMachine, rest easy")
        self.hue = EZHue()

        self.pot = MCP3008(channel=0)
        self.pot_value = -1
        print("Let's watch the pot switch")
        thread_it(lambda: self.watch_pot())
        print("Now how about a little infared")
        self.remote = IrRemote(when_pressed=self.when_ir_pressed)
        print("Chromecast be patient")
        self.chrome_cast = EZChromeCast("HomeCast")
        print("GPIO Time")
        Buttons.watch_button(self.LIGHT_BUTTON_PIN, self.toggle_lights, self.hue.on)
        Buttons.watch_button(self.CHROMECAST_BUTTON_PIN, self.toggle_chromecast, self.chrome_cast.playing)
        print("Alright dream cowboy, I'm ready for your button pressing")

    def when_ir_pressed(self, command):
        print("ir heard", command)
        if command is Command.Power:
            self.hue.toggle()
        elif command is Command.Play:
            self.chrome_cast.toggle()
        elif command is Command.Up:
            self.hue.brightness += .1
        elif command is Command.Down:
            self.hue.brightness -= .1
        elif command is Command.One:
            self.hue.set_color(HueColors.Blue)
        elif command is Command.Weird_Button:
            self.hue.disco_santa_clause()
        else:
            self.hue.make_lights_rando()

    def watch_pot(self):
        while True:
            # the pots a little noisy so lets ignore minor shifts
            if fabs(self.pot_value - self.pot.value) > .05:
                print("Brightness change", self.pot.value)
                self.pot_value = self.pot.value
                self.hue.brightness = self.pot_value
            time.sleep(0.05)

    def toggle_lights(self, on=None):
        self.hue.toggle(on)

    def toggle_chromecast(self, on=None):
        self.chrome_cast.toggle(on)

    @staticmethod
    def snooze():
        pass
