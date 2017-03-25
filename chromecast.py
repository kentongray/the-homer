from __future__ import print_function

import pychromecast

from util import thread_it


class EZChromeCast():
    def __init__(self, name="HomeCast", url="http://hpm.streamguys1.com/news-mp3", content_type="audio/mpeg"):
        self.content_type = content_type
        self.url = url
        self.cast = None
        thread_it(lambda: self.create_chrome_cast(name))
        self.playing = False
        self.ready = False

    def create_chrome_cast(self, name):
        self.cast = pychromecast.get_chromecast(friendly_name=name)
        self.cast.wait()
        self.playing = not self.cast.is_idle
        self.ready = True

    def play(self, url=None):
        if self.ready is False:
            return
        self.playing = True
        if url is None:
            url = self.url
        self.cast.media_controller.play_media(url, self.content_type)

    def toggle(self, on=None):
        if on is None:
            on = not self.playing
        print("chromecast coming ", on)
        if on:
            self.play()
        else:
            self.stop()

    def stop(self):
        if self.ready is False:
            return
        self.playing = False
        mc = self.cast.media_controller
        mc.stop()
