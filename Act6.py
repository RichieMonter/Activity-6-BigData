import requests
import json 

import requests
import json


API_KEY = "5914621c6060c844c16d2febc4ca98f8"

CITY = "Berlin"
COUNTRY_CODE = "DE" # Código para Alemania
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast" # API de pronóstico de 5 días / 3 horas

params = {
    'q': f"{CITY},{COUNTRY_CODE}",
    'appid': API_KEY,
    'units': 'metric' # Para obtener la temperatura en Celsius
}

try:
    # 1. Realizar la solicitud HTTP
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status() # Lanza un error si la solicitud falló

    # 2. Convertir la respuesta a formato JSON
    weather_data = response.json()

    print(f"Datos del pronóstico para {CITY} recopilados con éxito.")

    # 3. Guardar el resultado para análisis posterior
    with open('berlin_forecast.json', 'w') as f:
        json.dump(weather_data, f, indent=4)
        print("Datos guardados en 'berlin_forecast.json'.")

except requests.exceptions.HTTPError as err:
    print(f"Error al conectar con la API (revisa tu clave API y la ciudad): {err}")
except requests.exceptions.RequestException as err:
    print(f"Ocurrió un error en la solicitud: {err}")