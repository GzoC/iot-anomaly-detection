# Detección de Anomalías en Tiempo Real para IoT y Sistemas de Producción

Este proyecto está orientado a implementar un sistema robusto para detectar anomalías en tiempo real utilizando datos provenientes de dispositivos IoT (Internet of Things). Utiliza procesamiento de streaming, técnicas avanzadas de Machine Learning, visualización interactiva y prácticas de MLOps.

## 📌 Objetivos del Proyecto

- Implementar un pipeline de ingesta y procesamiento de datos en tiempo real.
- Aplicar modelos avanzados de Machine Learning para detectar anomalías en tiempo real.
- Crear un dashboard interactivo para visualizar anomalías y estados críticos.
- Automatizar todo el flujo con Docker y Kubernetes.
- Integrar prácticas modernas de CI/CD mediante GitHub Actions.

---

## 🛠️ Arquitectura Técnica

- **Kafka (Broker):** Recepción y gestión de streaming.
- **Spark Streaming (Procesamiento):** Limpieza, transformación, y agregación de datos.
- **ML Models (Python):** Isolation Forest, Autoencoders, LSTM para detección.
- **InfluxDB o PostgreSQL:** Almacenamiento y auditoría de datos.
- **Dashboard:** Visualización en tiempo real con Grafana o Streamlit.
- **Docker/Kubernetes:** Despliegue escalable de componentes.
- **GitHub Actions:** Automatización del flujo CI/CD.

---

## 🚀 Instalación y Configuración Inicial

### 1. Clonar repositorio:

```bash
git clone https://github.com/GzoC/anomaly-detection-iot.git
cd anomaly-detection-iot
```

### 2. Crear entorno virtual Python:

```bash
python -m venv venv
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 4. Iniciar Kafka con Docker:

```bash
cd docker
docker-compose up -d
```

---

## 📂 Estructura del Proyecto

```
anomaly-detection-iot/
├── data/
├── simulator/
├── streaming/
├── model/
├── dashboard/
├── docker/
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

---

## 🔜 Próximos pasos

- Entrenar e integrar modelos de ML.
- Desarrollar Dashboard en tiempo real.
- Automatización CI/CD.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

