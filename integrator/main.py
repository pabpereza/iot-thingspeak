import os
from dotenv import load_dotenv
from controllers.thingspeak_client import ThingSpeakClient
from controllers.tiempo_net import WeatherClient
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
        time.sleep(60)

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
    return templates.TemplateResponse("home.html",  {"request": request, "feeds": feeds["feeds"]})
