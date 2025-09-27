import pandas as pd
import json
import os

# --- 1. Definir Rutas de Archivos ---
WEATHER_FILE = "berlin_weather_forecast.json"
FLIGHTS_FILE = "berlin_flights.json"
OUTPUT_WEATHER_CSV = "transformed_weather_data.csv"
OUTPUT_FLIGHTS_CSV = "transformed_flights_data.csv"


# --- 2. Función de Transformación del Clima ---
def transform_weather_data(file_path):
    print(f"Transformando datos de clima de {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # El pronóstico está en la clave 'list'. Usamos json_normalize para aplanarlo.
        df_weather = pd.json_normalize(
            data['list'],
            sep='_',
            record_path=None
        )

        # Seleccionar y renombrar columnas clave para el análisis de scooters
        df_weather = df_weather[[
            'dt_txt', 'main_temp', 'main_feels_like', 'weather_0_description', 'wind_speed', 'pop'
        ]].rename(columns={
            'dt_txt': 'timestamp',
            'main_temp': 'temperatura_c',
            'main_feels_like': 'sensacion_termica_c',
            'weather_0_description': 'condicion_climatica',
            'wind_speed': 'velocidad_viento_m_s',
            'pop': 'probabilidad_precipitacion'
        })
        
        # Convertir a formato de fecha/hora
        df_weather['timestamp'] = pd.to_datetime(df_weather['timestamp'])

        print(f"Transformación de clima completada. Filas: {len(df_weather)}")
        return df_weather

    except Exception as e:
        print(f"Error al transformar datos de clima: {e}")
        return pd.DataFrame()


# --- 3. Función de Transformación de Vuelos ---
def transform_flights_data(file_path):
    print(f"Transformando datos de vuelos de {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Los datos de vuelos están en la clave 'data'
        # Usamos json_normalize, especificando los metadatos relevantes de los objetos anidados
        df_flights = pd.json_normalize(
            data['data'],
            sep='_',
            # Esto aplana las columnas de los diccionarios anidados (departure, arrival, flight)
        )
        
        # Seleccionar y renombrar columnas clave para el análisis de scooters
        df_flights = df_flights[[
            'flight_iata', 'departure_airport', 'arrival_scheduled'
        ]].rename(columns={
            'flight_iata': 'numero_vuelo',
            'departure_airport': 'aeropuerto_origen',
            'arrival_scheduled': 'hora_llegada_programada_utc'
        })
        
        # Convertir a formato de fecha/hora (y extraer solo la hora para el análisis de demanda)
        df_flights['hora_llegada_programada_utc'] = pd.to_datetime(df_flights['hora_llegada_programada_utc'])
        df_flights['hora_llegada_local'] = df_flights['hora_llegada_programada_utc'].dt.tz_convert('Europe/Berlin').dt.time
        
        print(f"Transformación de vuelos completada. Filas: {len(df_flights)}")
        return df_flights

    except Exception as e:
        print(f"Error al transformar datos de vuelos: {e}")
        return pd.DataFrame()


# --- 4. Ejecución Principal ---
if __name__ == "__main__":
    
    # 4.1 Transformar y guardar el clima
    df_clima = transform_weather_data(WEATHER_FILE)
    if not df_clima.empty:
        df_clima.to_csv(OUTPUT_WEATHER_CSV, index=False)
        print(f"Archivo de clima limpio guardado en: {OUTPUT_WEATHER_CSV}")

    # 4.2 Transformar y guardar los vuelos
    df_vuelos = transform_flights_data(FLIGHTS_FILE)
    if not df_vuelos.empty:
        df_vuelos.to_csv(OUTPUT_FLIGHTS_CSV, index=False)
        print(f"Archivo de vuelos limpio guardado en: {OUTPUT_FLIGHTS_CSV}")
        
    print("\n¡Transformación de datos completada! Listos para la carga en el Data Warehouse.")