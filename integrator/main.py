from controllers.thingspeak_client import ThingSpeakClient
from controllers.tiempo_es import WeatherClient

thingspeak_client = ThingSpeakClient(api_key="your_api_key", channel_id=12345)
weather_client = WeatherClient()

if __name__ == "__main__":

    # Ejemplo de uso de la API de El Tiempo
    province_code = "26"  # Código de provincia La Rioja
    municipality_code = "26018"  # Código de municipio de Arnedo (mi pueblo natal :D )

    print(f"Obteniendo datos del clima para provincia {province_code} y municipio {municipality_code}...")
    weather_data = weather_client.get_weather(province_code, municipality_code)

    print("Datos del clima recibidos:", weather_data)
