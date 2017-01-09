from math import floor
from random import randrange

from phue import Bridge


class EZHue:
    def __init__(self):
        self._brightness = 1
        print("Hue are you? (Hue Hue, Hue Hue)")
        self.bridge = self.create_bridge()
        self.on = self.bridge.get_light(1, 'on')
        print("Hue says hi! lights are currently ", self.on)

    @property
    def brightness(self):
        print("Getting value")
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        brightness = {'bri': floor(value * 255), 'transitiontime': 3}
        self.bridge.set_light(1, brightness)
        self.bridge.set_light(2, brightness)
        self.bridge.set_light(3, brightness)
        return self._brightness

    def toggle(self, on=None):
        if on is None:
            on = not self.on
        self.bridge.set_light([1, 2, 3], 'on', on)
        self.on = on

    def create_bridge(self):
        # look up the IP address using https://www.meethue.com/api/nupnp
        bridge = Bridge(Bridge.get_ip_address({}))
        # If the app is not registered and the button on the hub is not pressed,
        # press the button and cal l connect() (this only needs to be run a single time)
        bridge.connect()
        return bridge

    def rando_color(self):
        return {'hue': randrange(0, 65535), 'sat': randrange(0, 254), 'bri': randrange(0, 254),
                'transitiontime': 10}

    def make_lights_rando(self):
        self.bridge.set_light(1, self.rando_color())
        self.bridge.set_light(2, self.rando_color())
        self.bridge.set_light(3, self.rando_color())
