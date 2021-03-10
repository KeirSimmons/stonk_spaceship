from config import Config
from qhue import Bridge
import math

class HueStation:

    def __init__(self, lights=None, hub=None):
        self.config = Config().get("hue")
        self.client = Bridge(self.config["ip"], self.config["username"])
        self.light_names = lights
        self.get_lights()

    def get_lights(self):
        if self.light_names is None:
            self.lights = [self.client.lights[_id] for _id in self.client.lights().keys()]
        elif self.light_names not in self.config["lights"]:
            available_lights = list(self.config["lights"].keys())
            available_lights = " or ".join(available_lights)
            error_msg = f"Lights could not be found. Maybe you meant {available_lights}?"
            raise Exception(error_msg)
        else:
            self.lights = [self.client.lights[id] for id in self.config["lights"][self.light_names]]

    def change_colour(self, rgb, brightness=100):
        # brightness [0, 100] -> [0, 255]
        brightness = round(brightness / 100 * 255)
        xy = HueStation.rgb_to_xy(rgb)
        for light in self.lights:
            light.state(on=True, xy=xy, bri=brightness)

    def go_green(self, brightness=100):
        self.change_colour((0, 128, 0), brightness)

    def go_red(self, brightness=100):
        self.change_colour((255, 0, 0), brightness)

    def go_yellow(self, brightness=100):
        self.change_colour((255, 255, 0), brightness)

    def turn_off(self):
        for light in self.lights:
            light.state(on=False)

    @staticmethod
    def rgb_to_xy(rgb):
        R, G, B = [colour / 255 for colour in rgb]
        
        R = math.pow((R + 0.055) / (1.0 + 0.055), 2.4) if R > 0.04045 else R / 12.92
        G = math.pow((G + 0.055) / (1.0 + 0.055), 2.4) if G > 0.04045 else G / 12.92
        B = math.pow((B + 0.055) / (1.0 + 0.055), 2.4) if B > 0.04045 else B / 12.92

        X = R * 0.664511 + G * 0.154324 + B * 0.162028
        Y = R * 0.283881 + G * 0.668433 + B * 0.047685
        Z = R * 0.000088 + G * 0.072310 + B * 0.986039

        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)

        return [x, y]