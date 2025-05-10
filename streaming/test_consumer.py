# streaming/test_consumer.py

"""
Script para consumir mensajes desde el tópico Kafka 'iot_sensor_data' y mostrarlos por consola.

Creado por Gonzalo Cisterna Salinas - Proyecto IoT con Kafka y PySpark
"""

from kafka import KafkaConsumer
import json

# Configura el consumidor Kafka
consumer = KafkaConsumer(
    'iot_sensor_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # lee desde el inicio del tópico
    enable_auto_commit=True,
    group_id='iot_test_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Esperando mensajes del tópico 'iot_sensor_data'...\n")

# Ciclo que escucha y muestra los mensajes que llegan
try:
    for message in consumer:
        print(f"Mensaje recibido: {message.value}")
except KeyboardInterrupt:
    print("\nCerrando consumidor...")
    consumer.close()
