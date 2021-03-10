import json

class Config:
    def __init__(self):
        with open("config.json") as json_data_file:
            self.config = json.load(json_data_file)
            self.config["stonk_endpoint"] = self.config["stonk_endpoint"].replace(
                "{stonk}",
                self.get("stonk")
            )

    def get(self, key):
        return self.config[key]