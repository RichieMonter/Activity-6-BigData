import requests
import json
from datetime import datetime, timedelta

# --- 1. Define tus Parámetros ---

API_KEY_FLIGHTS = "53e268a26fec8e00581e8515e108505c"
BASE_URL_FLIGHTS = "http://api.aviationstack.com/v1/flights"
AIRPORT_IATA = "BER" # Código IATA para Berlín Brandeburgo
FLIGHT_STATUS = "scheduled" # Puedes probar con 'active' o 'landed'

# Calcula la fecha de hoy para el filtro (algunas APIs lo requieren)
# Aunque la API gratuita tiene limitaciones en fechas futuras, esta es la estructura.
today = datetime.now().strftime('%Y-%m-%d') 

# --- 2. Construye la Solicitud ---
params = {
    'access_key': API_KEY_FLIGHTS,
    'arr_iata': AIRPORT_IATA, # Filtrar por llegadas al aeropuerto BER
    'flight_status': FLIGHT_STATUS
    
}

print(f"Buscando vuelos de llegada para el aeropuerto {AIRPORT_IATA}...")

# --- 3. Realiza la Solicitud GET ---
try:
    response = requests.get(BASE_URL_FLIGHTS, params=params)
    response.raise_for_status()

    # --- 4. Procesa y Almacena la Respuesta JSON ---
    flights_data = response.json()

    print("Datos de vuelos recopilados con éxito.")

    # Ejemplo de procesamiento: Imprimir el resumen de los vuelos
    if 'data' in flights_data and flights_data['data']:
        print("\n--- Resumen de Vuelos de Llegada (ejemplos) ---")
        for flight in flights_data['data'][:5]: # Muestra los primeros 5
            flight_number = flight['flight']['iata']
            dep_city = flight['departure']['airport']
            arr_time = flight['arrival']['scheduled']
            
            print(f"Vuelo: {flight_number}, Origen: {dep_city}, Hora de Llegada Programada: {arr_time}")
    else:
        print("No se encontraron datos de vuelos de llegada en la respuesta.")

    # Guardar el JSON completo
    with open('berlin_flights.json', 'w') as f:
        json.dump(flights_data, f, indent=4)
        print("\nDatos completos de vuelos guardados en 'berlin_flights.json'")

except requests.exceptions.HTTPError as err:
    print(f"Error de HTTP: {err}")
    print(f"Respuesta de la API (revisa si la clave es válida): {response.text}")
except requests.exceptions.RequestException as err:
    print(f"Error al realizar la solicitud: {err}")