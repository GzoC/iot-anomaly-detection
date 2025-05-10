# streaming/test_consumer.py
# -*- coding: utf-8 -*-
"""
Script para consumir mensajes del tópico Kafka 'iot_sensor_data'
y mostrarlos por consola.

Creado por Gonzalo Cisterna Salinas - github.com/GzoC
"""

from kafka import KafkaConsumer
import json

# Creamos el consumidor de Kafka
consumer = KafkaConsumer(
    'iot_sensor_data',                      # Tópico al que se suscribe
    bootstrap_servers='localhost:9092',     # Dirección del broker de Kafka
    auto_offset_reset='earliest',           # Comienza desde el inicio del tópico
    enable_auto_commit=True,                # Kafka guardará automáticamente el desplazamiento
    group_id='iot-test-group-1',            # ID del grupo de consumidores (puedes cambiarlo si no ves mensajes)
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserializa los mensajes de JSON
)

print("🟢 Esperando mensajes del tópico 'iot_sensor_data'...")

# Loop infinito para escuchar mensajes
for message in consumer:
    print(f"📩 Mensaje recibido: {message.value}")
