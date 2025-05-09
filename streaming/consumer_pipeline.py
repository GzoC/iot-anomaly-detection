# consumer_pipeline.py

import time                                      # Para manejar intervalos y pausas
import json                                      # Para parsear mensajes JSON de Kafka
from kafka import KafkaConsumer                  # Cliente Kafka en Python
import pandas as pd                              # Para crear DataFrames y procesarlos
from sqlalchemy import create_engine             # Para conectar y escribir en la base de datos

# ——————————————————————————————————————————————————————————————————————————
# 1. CONFIGURACIÓN
# ——————————————————————————————————————————————————————————————————————————
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']     # Dirección del broker Kafka
KAFKA_TOPIC = 'iot_sensor_data'                  # Tópico donde el simulador publica
BATCH_INTERVAL = 5                               # Duración de cada ventana (en segundos)
DB_CONNECTION_STRING = (                           # Cadena de conexión a PostgreSQL
    'postgresql://usuario:password@localhost:5432/iotdb'
)

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
        KAFKA_TOPIC,                             # Tópico a suscribir
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Deserializar JSON
        auto_offset_reset='latest',             # Leer solo nuevos mensajes
        enable_auto_commit=True,                # Confirmar offsets automáticamente
        group_id='iot-consumer-group'           # ID de grupo para coordinar consumidores
    )

    # 2.2 Crear motor de base de datos
    engine = create_engine(DB_CONNECTION_STRING)

    buffer = []                                 # Lista temporal para acumular mensajes
    last_flush = time.time()                    # Marca de tiempo de la última escritura

    # 2.3 Bucle infinito de consumo
    for message in consumer:
        buffer.append(message.value)            # Añadir el mensaje al buffer

        # 2.4 Cuando supera el intervalo definido, procesar el batch
        if time.time() - last_flush >= BATCH_INTERVAL:
            # 2.4.1 Convertir buffer en DataFrame de pandas
            df = pd.DataFrame(buffer)

            # 2.4.2 Limpieza de datos: eliminar filas con valores nulos
            df = df.dropna()

            # 2.4.3 Conversión de tipos: timestamp a datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # 2.4.4 Agregaciones por sensor (media de cada métrica)
            aggregated = df.groupby('sensor_id').agg({
                'temperature': 'mean',
                'vibration': 'mean',
                'pressure': 'mean',
                'voltage': 'mean'
            }).reset_index()

            # 2.4.5 Escribir batch agregado en la tabla 'sensor_metrics'
            aggregated.to_sql(
                'sensor_metrics',
                engine,
                if_exists='append',               # Añadir registros sin borrar existentes
                index=False                       # No escribir índice como columna
            )

            print(f"Escritos {len(aggregated)} registros en la base de datos")

            # 2.4.6 Resetear buffer y actualizar marca de tiempo
            buffer = []
            last_flush = time.time()

if __name__ == '__main__':
    main()  # Ejecutar la función principal
