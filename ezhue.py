from enum import Enum
from math import floor
from random import randrange

from phue import Bridge


class HueColors(Enum):
    Blue = {'hue': 46920, 'sat': 255, 'transitiontime': 5, 'effect': 'none'}
    White = {'hue': 46920, 'sat': 0, 'transitiontime': 5, 'effect': 'none'}
    Red = {'hue': 26920, 'sat': 255, 'transitiontime': 5, 'effect': 'none'}


class EZHue:
    def __init__(self):
        self._brightness = 1
        print("Hue are you? (Hue Hue, Hue Hue)")
        self.bridge = self.create_bridge()
        print("bridge made")
        self.on = self.bridge.get_light(1, 'on')
        print("Hue says hi! lights are currently ", self.on)

    @property
    def brightness(self):
        print("Getting value")
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = min(1, max(value, 0))
        print("brightness", self._brightness)
        brightness = {'bri': floor(self._brightness * 255), 'transitiontime': 3}
        self.bridge.set_light([1, 2, 3], brightness)
        return self._brightness

    def toggle(self, on=None):
        if on is None:
            on = not self.on
        self.bridge.set_light([1, 2, 3], 'on', on)
        self.on = on

    def create_bridge(self):
        # look up the IP address using https://www.meethue.com/api/nupnp
        bridge = Bridge()
        # If the app is not registered and the button on the hub is not pressed,
        # press the button and cal l connect() (this only needs to be run a single time)
        bridge.connect()
        return bridge

    def rando_color(self):
        return {'hue': randrange(0, 65535), 'sat': randrange(200, 255),
                'transitiontime': 10, 'effect': 'none'}

    def disco_santaclause(self):
        return self.bridge.set_light([1, 2, 3], {'effect': 'colorloop'})

    def make_lights_rando(self):
        print("random lights time")
        self.bridge.set_light(1, self.rando_color())
        self.bridge.set_light(2, self.rando_color())
        self.bridge.set_light(3, self.rando_color())

    def set_color(self, color):
        print(color)
        self.bridge.set_light([1, 2, 3], color.value)
