# Importa la librería 'requests' para manejar las peticiones HTTP a la API.
import requests
# Importa la librería 'json' para el procesamiento y formateo de datos JSON.
import json
# Importa la funcionalidad de tiempo para trabajar con la fecha actual.
from datetime import datetime, timedelta

# --- 1. Define tus Parámetros ---

# Define la clave de la API de AviationStack para autenticación.
API_KEY_FLIGHTS = "53e268a26fec8e00581e8515e108505c"
# Define la URL base para el endpoint de vuelos en la API.
BASE_URL_FLIGHTS = "http://api.aviationstack.com/v1/flights"
# Define el código IATA del aeropuerto a filtrar (CDG: París, Francia). (REQUISITO: CAMBIO DE PAÍS)
AIRPORT_IATA = "CDG" 
# Define el estado del vuelo que se desea consultar.
FLIGHT_STATUS = "scheduled" 

# Calcula la fecha y la formatea para ser usada como filtro si es necesario.
# La variable 'today' almacena la fecha actual en formato AAAA-MM-DD.
today = datetime.now().strftime('%Y-%m-%d') 

# --- 2. Construye la Solicitud ---
# Define los parámetros de la solicitud HTTP en un diccionario.
params = {
    # Clave de acceso requerida por la API de AviationStack.
    'access_key': API_KEY_FLIGHTS,
    # Filtra por vuelos cuya llegada sea al aeropuerto definido (CDG).
    'arr_iata': AIRPORT_IATA, 
    # Filtra por vuelos que tienen el estado programado.
    'flight_status': FLIGHT_STATUS
}

# Imprime un mensaje indicando la acción que se va a realizar.
print(f"Buscando vuelos de llegada para el aeropuerto {AIRPORT_IATA}...")

# --- 3. Realiza la Solicitud GET ---
# Inicia un bloque 'try' para capturar posibles errores durante la solicitud.
try:
    # Realiza la petición GET a la API con la URL base y los parámetros.
    response = requests.get(BASE_URL_FLIGHTS, params=params)
    # Lanza una excepción si la solicitud HTTP ha fallado (código 4xx o 5xx).
    response.raise_for_status()

    # --- 4. Procesa y Almacena la Respuesta JSON ---
    # Convierte la respuesta exitosa en un objeto JSON de Python.
    flights_data = response.json()

    # Imprime la confirmación de la recopilación de datos.
    print("Datos de vuelos recopilados con éxito.")

    # Inicia el procesamiento: verifica si la respuesta contiene datos válidos en la clave 'data'.
    if 'data' in flights_data and flights_data['data']:
        # Imprime un encabezado para el resumen de los datos.
        print("\n--- Resumen de Vuelos de Llegada (ejemplos) ---")
        # Itera sobre los primeros 5 vuelos en la lista de datos.
        for flight in flights_data['data'][:5]: 
            # Extrae el número de vuelo (código IATA del vuelo).
            flight_number = flight['flight']['iata']
            # Extrae el aeropuerto de origen.
            dep_city = flight['departure']['airport']
            # Extrae la hora de llegada programada.
            arr_time = flight['arrival']['scheduled']
            
            # Imprime la información resumida de cada vuelo.
            print(f"Vuelo: {flight_number}, Origen: {dep_city}, Hora de Llegada Programada: {arr_time}")
    else:
        # Mensaje si la API devuelve una respuesta exitosa pero sin datos de vuelo.
        print("No se encontraron datos de vuelos de llegada en la respuesta.")

    # Guardar el JSON completo en un archivo local.
    # Abre el archivo en modo escritura.
    with open('paris_flights.json', 'w') as f:
        # Escribe el objeto JSON completo en el archivo con indentación.
        json.dump(flights_data, f, indent=4)
        # Informa al usuario sobre la ubicación del archivo guardado.
        print("\nDatos completos de vuelos guardados en 'paris_flights.json'")

# Captura errores de HTTP específicos de la librería requests.
except requests.exceptions.HTTPError as err:
    # Imprime el error HTTP y el mensaje de la API para depuración.
    print(f"Error de HTTP: {err}")
    print(f"Respuesta de la API (revisa si la clave es válida): {response.text}")
# Captura errores generales al realizar la solicitud.
except requests.exceptions.RequestException as err:
    # Imprime un mensaje para errores de conexión o solicitud.
    print(f"Error al realizar la solicitud: {err}")
