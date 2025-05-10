# streaming/test_consumer.py

"""
Script para consumir mensajes desde el tópico Kafka 'iot_sensor_data' y mostrarlos por consola.

Creado por Gonzalo Cisterna Salinas - Proyecto IoT con Kafka y PySpark
"""

# streaming/test_consumer.py

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'iot_sensor_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # <-- Esta línea es clave
    enable_auto_commit=True,
    group_id='iot-group',
    value_serializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Esperando mensajes...")
for message in consumer:
    print(f"Mensaje recibido: {message.value}")
