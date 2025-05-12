import requests

class ThingSpeakClient:
    def __init__(self, api_key: str, channel_id: int):
        self.api_key = api_key
        self.channel_id = channel_id
        self.base_url = "https://api.thingspeak.com"

    def send_data(self, field: str, value: float):
        url = f"{self.base_url}/update"
        params = {
            "api_key": self.api_key,
            field: value
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def read_data(self):
        url = f"{self.base_url}/channels/{self.channel_id}/feeds.json"
        params = {
            "api_key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
