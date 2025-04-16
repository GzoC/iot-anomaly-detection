# iot_data_simulator.py

import json
import random
import time
from kafka import KafkaProducer
from datetime import datetime

# Configuración del Productor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Función para generar datos simulados del sensor
def generate_sensor_data():
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20.0, 100.0), 2),
        "vibration": round(random.uniform(0.0, 5.0), 2),
        "pressure": round(random.uniform(30.0, 200.0), 2),
        "voltage": round(random.uniform(200.0, 240.0), 2)
    }
    return data

# Bucle principal para enviar datos continuamente hacia Kafka
def send_data():
    topic = 'iot_sensor_data'
    try:
        while True:
            sensor_data = generate_sensor_data()
            producer.send(topic, sensor_data)
            print(f"Enviado: {sensor_data}")
            time.sleep(1)  # Envía datos cada segundo
    except KeyboardInterrupt:
        print("Envío interrumpido por el usuario.")

# Ejecución del simulador
if __name__ == '__main__':
    send_data()
