# streaming/test_producer.py

"""
Script para enviar mensajes de prueba al tópico 'iot_sensor_data' de Kafka.

Creado por Gonzalo Cisterna Salinas - Proyecto de Análisis IoT con Kafka y PySpark
"""

from kafka import KafkaProducer
import json
import time

# Configura el productor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Lista de mensajes de ejemplo
messages = [
    {"device_id": "sensor_01", "timestamp": "2025-05-08T21:00:00", "temperature": 23.5, "humidity": 45},
    {"device_id": "sensor_02", "timestamp": "2025-05-08T21:00:05", "temperature": 24.1, "humidity": 50},
    {"device_id": "sensor_03", "timestamp": "2025-05-08T21:00:10", "temperature": 22.8, "humidity": 42}
]

# Envía los mensajes uno a uno con un pequeño retardo
for msg in messages:
    producer.send("iot_sensor_data", msg)
    print(f"Mensaje enviado: {msg}")
    time.sleep(1)  # espera 1 segundo entre envíos

# Cierra la conexión del productor
producer.close()
