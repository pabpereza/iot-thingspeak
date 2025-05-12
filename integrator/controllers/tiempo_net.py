import requests

class WeatherClient:
    def __init__(self, base_url: str = "https://www.el-tiempo.net/api/json/v2", 
                 province_code: str = "01", municipality_code: str = "001"):
        self.base_url = base_url
        self.province_code = province_code
        self.municipality_code = municipality_code

    def get_weather(self):
        url = f"{self.base_url}/provincias/{self.province_code}/municipios/{self.municipality_code}"
        response = requests.get(url)
        if response.status_code == 200:
            
            # Obtener temperatura y humedad
            data = response.json()
            temperature = data['temperatura_actual']
            humidity = data['humedad']

            return temperature, humidity
        else:
            response.raise_for_status()