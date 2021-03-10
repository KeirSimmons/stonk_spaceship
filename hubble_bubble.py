from config import Config

from googlecontroller import GoogleAssistant
from googlecontroller.http_server import serve_file # for local files

import time

class HubbleBubble:
    def __init__(self):
        self.config = Config()
        self._host = self.config.get("google_home")["ip"]
        self.home = GoogleAssistant(host=self._host)

    def say(self, msg):
        self.home.say(msg)

    def error(self, msg):
        self.say(msg)
        raise Exception(msg)

    def alarm(self, msg):
        self.say(msg)
        time.sleep(5)
        self.home.play("http://www.hubharp.com/web_sound/BachGavotteShort.mp3")