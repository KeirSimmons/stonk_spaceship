from config import Config
from hue_station import HueStation
from hubble_bubble import HubbleBubble

import requests
import math, time

class Stonks:
    def __init__(self):
        self.config = Config()
        self.hue_station = HueStation()
        self.home = HubbleBubble()
        self.prices = []
        self.timestamps = []

        self.start()

    def start(self):
        while True:
            price, timestamp = self.query_yahoo()
            moved = self.add_price(price, timestamp)
            self.go_ape()
            if moved:
                self.notification(price)
            time.sleep(3)

    def add_price(self, price, timestamp):
        if len(self.timestamps) and self.timestamps[-1] == timestamp:
            return False
        else:
            self.timestamps.append(timestamp)
            self.prices.append(price)

            if len(self.prices) == 1:
                return False

            current_price = self.prices[-1]
            previous_price = self.prices[-2]

            if len(self.timestamps) > 10:
                self.timestamps = self.timestamps[1:]
                self.prices = self.prices[1:]

            if abs(current_price - previous_price) > self.config.get("alert_on_jump"):
                return True

            if current_price > self.config.get("alarm")["high"]:
                self.alarm("good")
                time.sleep(15)
            elif current_price < self.config.get("alarm")["low"]:
                self.alarm("bad")
                time.sleep(15)

            return False

    def query_yahoo(self):
        data = requests.get(self.config.get("stonk_endpoint")).json()
        meta_data = data['chart']['result'][0]['meta']
        price = +meta_data['regularMarketPrice']
        timestamp = meta_data['regularMarketTime']
        # currency = meta_data['currency']
        return price, timestamp

    def stonk_movement(self, direction, price=0):
        if direction == "up":
            self.hue_station.go_green()
        elif direction == "down":
            self.hue_station.go_red()
        else:
            self.hue_station.go_yellow()

    def go_ape(self):
        if len(self.timestamps) > 1:
            if self.prices[-1] > self.prices[-2]:
                self.stonk_movement("up")
            elif self.prices[-1] == self.prices[-2]:
                self.stonk_movement("neutral")
            else:
                self.stonk_movement("down")
        else:
            self.stonk_movement("neutral")
    
    def notification(self, price):
        self.home.say(f"{self.config.get('stonk')} is {price}")

    def alarm(self, mood):
        price = self.prices[-1]
        if mood == "good":
            self.hue_station.go_green()
            self.config.config["alarm"]["high"] += 1
            self.home.alarm(f"WE'RE GOING TO THE MOON AT {price}!")
        else:
            self.hue_station.go_red()
            self.config.config["alarm"]["low"] -= 1
            self.home.alarm(f"STONK CRASHING AT {price}!")
        #self.home.volume(100)

if __name__ == "__main__":
    Stonks()