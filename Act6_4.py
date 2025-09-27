from google.cloud import bigquery
import os

# --- 1. Define tus Parámetros ---
PROJECT_ID = "tu-id-de-proyecto-gcp" # Ejemplo: 'scooter-bigdata-project'
DATASET_NAME = "berlin_scooter_data" # Nombre que darás al conjunto de datos
TABLE_NAME = "flights_arrivals_clean"  # Nombre de la tabla de destino
SOURCE_FILE = "transformed_flights_data.csv" # Archivo CSV limpio de la Act. 6.4

# --- 2. Inicializar el Cliente de BigQuery ---
try:
    client = bigquery.Client(project=PROJECT_ID)
    print(f"Conectado a BigQuery en proyecto: {PROJECT_ID}")
except Exception as e:
    print(f"Error al inicializar cliente de BigQuery: {e}")
    exit()

# --- 3. Crear el Dataset (Si no existe) ---
dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "EU" # Los datos de Europa se almacenan comúnmente en la UE
try:
    client.create_dataset(dataset, timeout=30)
    print(f"Dataset '{DATASET_NAME}' creado o ya existe.")
except Exception:
    # Si ya existe, se lanzará una excepción, lo cual ignoramos
    pass

# --- 4. Configurar el Trabajo de Carga ---
table_id = f"{dataset_id}.{TABLE_NAME}"
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,  # Ignorar la fila de encabezados
    autodetect=True,      # BigQuery intentará detectar los tipos de columna automáticamente
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Sobrescribir la tabla si existe
)

# --- 5. Iniciar la Carga ---
print(f"\nIniciando la carga de {SOURCE_FILE} en la tabla {table_id}...")

try:
    with open(SOURCE_FILE, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    # Esperar a que el trabajo de carga finalice
    job.result() 
    print(f"Carga finalizada con éxito. Filas cargadas: {job.output_rows}")

except FileNotFoundError:
    print(f"¡ERROR! No se encontró el archivo de origen: {SOURCE_FILE}. Asegúrate de que el CSV limpio existe.")
except Exception as e:
    print(f"Error durante la carga en BigQuery: {e}")