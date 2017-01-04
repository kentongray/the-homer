from random import randrange
from math import floor
from phue import Bridge


class EZHue:
    def __init__(self):
        print("Hue are you? (Hue Hue, Hue Hue)")
        self.bridge = self.create_bridge()
        self.on = self.bridge.get_light(1, 'on')
        print("Hue says hi! I'm currently ", self.on)

    def toggle(self, on=None):
        if on is None:
            on = not self.on
        self.bridge.set_light([1, 2, 3], 'on', on)

    def create_bridge(self):
        # look up the IP address using https://www.meethue.com/api/nupnp
        bridge = Bridge(Bridge.get_ip_address({}))
        # If the app is not registered and the button on the hub is not pressed,
        # press the button and call connect() (this only needs to be run a single time)
        bridge.connect()
        return bridge

    def brightness(self, brightness):
       brightness = {'bri': floor(brightness * 255), 'transitiontime': 3}
       self.bridge.set_light(1, brightness)
       self.bridge.set_light(2, brightness)
       self.bridge.set_light(3, brightness)
       return brightness

    def rando_color(self):
        return {'hue': randrange(0, 65535), 'sat': randrange(0, 254), 'bri': randrange(0, 254),
                'transitiontime': 10}

    def make_lights_rando(self, on):
        self.bridge.set_light(1, self.rando_color())
        self.bridge.set_light(2, self.rando_color())
        self.bridge.set_light(3, self.rando_color())
