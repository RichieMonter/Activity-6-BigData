# Importa la librería 'requests' para manejar las peticiones HTTP a la API.
import requests
# Importa la librería 'json' para trabajar con la respuesta en formato JSON.
import json 

# --- Configuración de la API y la Ubicación (Cambio Obligatorio) ---

# Define la clave de la API (API Key) para autenticar la solicitud. (Usando la clave que proporcionaste).
API_KEY = "5914621c6060c844c16d2febc4ca98f8"

# Define la nueva ciudad para recopilar los datos (Cambio requerido por el instructor).
CITY = "Paris"
# Define el código de país (ISO 3166) para la nueva ciudad.
COUNTRY_CODE = "FR" 
# Define la URL base para el endpoint de pronóstico de 5 días / 3 horas.
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# --- Definición de Parámetros de Solicitud ---

# Define los parámetros que se enviarán en la solicitud HTTP (Diccionario de Python).
params = {
    # Combina la ciudad y el código de país para el parámetro 'q'.
    'q': f"{CITY},{COUNTRY_CODE}",
    # Asigna la clave de la API al parámetro 'appid'.
    'appid': API_KEY,
    # Especifica 'metric' para obtener las temperaturas en Celsius.
    'units': 'metric' 
}

# --- Ejecución y Manejo de Errores ---

# Inicia un bloque 'try' para capturar posibles errores de conexión o HTTP.
try:
    # 1. Realiza la solicitud GET HTTP a la URL base con los parámetros definidos.
    response = requests.get(BASE_URL, params=params)
    # Lanza una excepción si el estado de la respuesta HTTP indica un error (4xx o 5xx).
    response.raise_for_status() 

    # 2. Convierte la respuesta HTTP exitosa (cuerpo de la respuesta) a un objeto JSON.
    weather_data = response.json()

    # Imprime un mensaje de éxito indicando que los datos fueron recopilados.
    print(f"Datos del pronóstico para {CITY} recopilados con éxito.")

    # 3. Guardar el resultado en un archivo JSON local para análisis posterior.
    # Abre el archivo en modo escritura ('w').
    with open('paris_forecast.json', 'w') as f:
        # Escribe el objeto JSON en el archivo, usando indentación para facilitar la lectura.
        json.dump(weather_data, f, indent=4)
        # Imprime un mensaje que indica dónde se guardaron los datos.
        print("Datos guardados en 'paris_forecast.json'.")

# Captura errores específicos de peticiones HTTP (ej: 401, 404, 500).
except requests.exceptions.HTTPError as err:
    # Imprime el mensaje de error HTTP si la solicitud falló.
    print(f"Error al conectar con la API (revisa tu clave API y la ciudad): {err}")
# Captura errores generales de la librería requests (ej: problemas de red/DNS).
except requests.exceptions.RequestException as err:
    # Imprime el mensaje de error general de la solicitud.
    print(f"Ocurrió un error en la solicitud: {err}")