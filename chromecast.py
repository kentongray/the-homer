from __future__ import print_function

import pychromecast


class EZChromeCast():
    def __init__(self, name="HomeCast", url="http://hpm.streamguys1.com/news-mp3", content_type="audio/mpeg"):
        self.content_type = content_type
        self.url = url
        self.playing = False
        self.cast = pychromecast.get_chromecast(friendly_name=name)
        self.cast.wait()

    def play(self, url=None):
        if url is None:
            url = self.url
        self.cast.media_controller.play_media(url, self.content_type)
        self.playing = True

    def stop(self):
        mc = self.cast.media_controller
        mc.stop()
        self.playing = False
