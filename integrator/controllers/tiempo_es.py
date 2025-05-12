import requests

class WeatherClient:
    def __init__(self, base_url: str = "https://www.el-tiempo.net/api/json/v2"):
        self.base_url = base_url

    def get_weather(self, province_code: str, municipality_code: str):
        url = f"{self.base_url}/provincias/{province_code}/municipios/{municipality_code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()