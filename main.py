import os
from dotenv import load_dotenv
from controllers.thingspeak_client import ThingSpeakClient
from controllers.tiempo_net import WeatherClient
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from datetime import datetime
import subprocess
import threading
import time
from pytz import timezone

#### VARIABLES Y CONFIGURACIONES ####
# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener variables de entorno
ts_api_key = os.getenv("TS_API_KEY")
ts_channel_id = os.getenv("TS_CHANNEL_ID")
tiempo_province_code = os.getenv("TIEMPO_PROVINCE_CODE")
tiempo_municipality_code = os.getenv("TIEMPO_MUNICIPALITY_CODE")

# Leer el API key de ThingSpeak desde las variables de entorno
api_key = os.getenv("THINGSPEAK_API_KEY")


# Crear instancia de FastAPI
app = FastAPI()

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="views")

def datetimeformat(value):
    madrid_tz = timezone('Europe/Madrid')
    utc_time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    local_time = utc_time.astimezone(madrid_tz)
    return local_time.strftime("%d-%m-%Y %H:%M:%S")

templates.env.filters['datetimeformat'] = datetimeformat

# -------------------------------------------#
#### INSTANCIAS DE CLIENTES Y FUNCIONES ####
# Crear instancias de los clientes a partir de las clases de /controllers
thingspeak_client = ThingSpeakClient(api_key=ts_api_key, channel_id=ts_channel_id)
weather_client = WeatherClient(province_code=tiempo_province_code,municipality_code=tiempo_municipality_code)

# Función para obtener los datos del cliema y cargar los datos en ThingSpeak
def update_data():
    # Obteniendo datos del clima 
    temperature, humedity = weather_client.get_weather()
    # Registrando datos de temperatura y humedad en ThingSpeak
    thingspeak_client.send_data(field1="field1", field2="field2", value1=temperature, value2=humedity)

# Función para ejecutar update_data cada minuto
def schedule_update_data():
    while True:
        update_data()
        time.sleep(3600)

# Lanzar un subproceso para ejecutar la función periódicamente
def start_update_data_subprocess():
    thread = threading.Thread(target=schedule_update_data, daemon=True)
    thread.start()

# Iniciar el subproceso al arrancar la aplicación
start_update_data_subprocess()

#--------------------------------------------#
## RUTAS / ENDPOINTS ##
@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    feeds = thingspeak_client.read_data()
    # Ordenar los feeds por fecha
    feeds["feeds"].sort(key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    return templates.TemplateResponse("home.html",  {"request": request, "feeds": feeds["feeds"]})

@app.get("/update")
def update_endpoint():
    update_data()
    return RedirectResponse(url="/")

@app.post("/add-data")
def add_data_endpoint(data: dict):
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    if temperature is not None and humidity is not None:
        # Registrar los datos manualmente en ThingSpeak
        thingspeak_client.send_data(field1="field1", field2="field2", value1=temperature, value2=humidity)
        return {"message": "Datos cargados correctamente"}
    else:
        return {"error": "Faltan datos"}, 400

@app.get("/forecast")
def get_forecast():
    # Simulación de datos de previsión para los próximos 7 días
    forecast_data = [
        {"date": "2025-05-13", "description": "Soleado", "temp": 25},
        {"date": "2025-05-14", "description": "Parcialmente nublado", "temp": 22},
        {"date": "2025-05-15", "description": "Lluvias ligeras", "temp": 20},
        {"date": "2025-05-16", "description": "Nublado", "temp": 18},
        {"date": "2025-05-17", "description": "Soleado", "temp": 24},
        {"date": "2025-05-18", "description": "Tormentas", "temp": 19},
        {"date": "2025-05-19", "description": "Soleado", "temp": 26},
    ]
    return forecast_data
