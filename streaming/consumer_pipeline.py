# streaming/consumer_pipeline.py

import time                        # Para manejar intervalos y pausas
import json                        # Para parsear mensajes JSON de Kafka
import os                          # Para leer variables de entorno
from kafka import KafkaConsumer     # Cliente Kafka en Python
import pandas as pd                # Para crear DataFrames y procesarlos
from sqlalchemy import create_engine
from dotenv import load_dotenv     # Para cargar .env

# ——————————————————————————————————————————————————————————————————————————
# 1. CARGA DE VARIABLES DE ENTORNO
# ——————————————————————————————————————————————————————————————————————————
# Carga las variables definidas en el archivo .env ubicado en la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), os.pardir, '.env')
load_dotenv(dotenv_path=env_path)

# Obtener valores del entorno
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS').split(',')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
BATCH_INTERVAL = int(os.getenv('BATCH_INTERVAL', '5'))
DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

# ——————————————————————————————————————————————————————————————————————————
# 2. FUNCIÓN PRINCIPAL
# ——————————————————————————————————————————————————————————————————————————
def main():
    """
    Crea un consumidor Kafka, acumula mensajes en ventanas de tiempo,
    los convierte en un DataFrame, aplica limpieza y agregaciones,
    y escribe los resultados en una tabla de PostgreSQL.
    """

    # 2.1 Crear consumidor Kafka
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=os.getenv('KAFKA_CONSUMER_GROUP', 'iot-consumer-group')
    )

    # 2.2 Crear motor de base de datos
    engine = create_engine(DB_CONNECTION_STRING)

    buffer = []                                # Lista temporal para mensajes
    last_flush = time.time()                   # Marca de tiempo de la última escritura

    # 2.3 Bucle infinito de consumo
    for message in consumer:
        buffer.append(message.value)

        # 2.4 Procesar batch cuando expire la ventana
        if time.time() - last_flush >= BATCH_INTERVAL:
            df = pd.DataFrame(buffer)          # 2.4.1 Convertir buffer a DataFrame

            df = df.dropna()                   # 2.4.2 Eliminar valores nulos
            df['timestamp'] = pd.to_datetime(df['timestamp'])  # 2.4.3 Convertir timestamp

            # 2.4.4 Agregación por sensor
            aggregated = df.groupby('sensor_id').agg({
                'temperature': 'mean',
                'vibration': 'mean',
                'pressure': 'mean',
                'voltage': 'mean'
            }).reset_index()

            # 2.4.5 Escritura en la tabla 'sensor_metrics'
            aggregated.to_sql(
                'sensor_metrics',
                engine,
                if_exists='append',
                index=False
            )

            print(f"Escritos {len(aggregated)} registros en la base de datos")

            buffer = []                        # 2.4.6 Limpieza del buffer
            last_flush = time.time()          # Actualizar marca de tiempo

if __name__ == '__main__':
    main()  # Ejecutar la función principal
