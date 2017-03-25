import time
from math import fabs

import RPi.GPIO as GPIO
from gpiozero import MCP3008
from gpiozero import Button
from nester import Nester
from chromecast import EZChromeCast
from ezhue import EZHue, HueColors
from irremote import IrRemote, Command
from util import thread_it


class DreamMachine:
    LIGHT_BUTTON_PIN = 21
    CHROMECAST_BUTTON_PIN = 16
    RANDO_PIN = 20
    IR_PIN = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_BUTTON_PIN, GPIO.IN)
    GPIO.setup(CHROMECAST_BUTTON_PIN, GPIO.IN)

    def __init__(self, cfg=None):
        self.nest = Nester(cfg)
        print("Starting the DreamMachine, rest easy...")
        self.hue = EZHue()

        self.pot = MCP3008(channel=0)
        self.pot_value = -1
        print("Let's watch the pot switch")
        thread_it(lambda: self.watch_pot())
        print("Now how about a little infared")
        #self.remote = IrRemote(pin=DreamMachine.IR_PIN, when_pressed=self.when_ir_pressed)
        print("Chromecast be patient")
        self.chrome_cast = EZChromeCast("HomeCast")
        print("GPIO Time")
        self.light_button = Button(self.LIGHT_BUTTON_PIN, pull_up=False)
        self.chromecast_button = Button(self.CHROMECAST_BUTTON_PIN, pull_up=False)
        self.sleep_button = Button(self.RANDO_PIN, pull_up=False)

        self.light_button.when_pressed = self.toggle_lights
        self.chromecast_button.when_pressed = self.toggle_chromecast
        self.sleep_button.when_pressed = self.take_me_to_the_zen_garden

        print("Alright dream cowboy, I'm ready for your button pressing")

    def take_me_to_the_zen_garden(self):
        print("the door is very old")
        self.chrome_cast.play("http://172.16.0.20/static/zengarden.mp3")

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
            self.hue.disco_santa_claus()
        else:
            self.hue.make_lights_rando()

    def watch_pot(self):
        pass
        # while True:
        #     # the pots a little noisy so lets ignore minor shifts
        #     if fabs(self.pot_value - self.pot.value) > .05:
        #         print("Brightness change", self.pot.value)
        #         self.pot_value = self.pot.value
        #         self.hue.brightness = self.pot_value
        #     time.sleep(0.05)

    def rando(self, on=None):
        print("setting a random color")
        self.hue.toggle(True)
        self.hue.rando_color()

    def toggle_lights(self, on=None):
        print("toggling lights")
        self.hue.toggle(on)
        self.hue.brightness = .9

    def toggle_chromecast(self, on=None):
        self.chrome_cast.toggle(on)

    @staticmethod
    def snooze():
        pass
