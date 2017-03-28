from __future__ import print_function

import pychromecast

from util import thread_it


class EZChromeCast():
    def __init__(self, name="HomeCast", url="http://hpm.streamguys1.com/news-mp3", content_type="audio/mpeg"):
        self.content_type = content_type
        self.url = url
        self.cast = None
        thread_it(lambda: self.create_chrome_cast(name))
        self.ready = False

    @property
    def playing(self):
        return self.ready and not self.cast.is_idle

    def create_chrome_cast(self, name):
        self.cast = pychromecast.get_chromecast(friendly_name=name)
        self.cast.wait()
        self.ready = True

    def play(self, url=None):
        if self.ready is False:
            print("chromecast isn't ready yet")
            return
        if url is None:
            url = self.url
        print("playing", url)
        self.cast.media_controller.play_media(url, self.content_type)
        print(self.cast.status)
        print(self.cast.media_controller.status)

    def toggle(self, on=None):
        if on is None:
            on = not self.playing

        if on:
            self.play()
        else:
            self.stop()

    def stop(self):
        if self.ready is False:
            return
        mc = self.cast.media_controller
        mc.stop()
