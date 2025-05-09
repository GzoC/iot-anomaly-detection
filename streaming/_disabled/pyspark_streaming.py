"""
    # pyspark_streaming.py
    # -----------------------------------------------------------
    # Este script implementa un ejemplo básico de "Structured Streaming"
    # usando PySpark para leer datos en tiempo real desde Kafka,
    # transformarlos y mostrarlos en la consola.
    # -----------------------------------------------------------


    #PASOS PARA EJECUTAR ESTE SCRIPT:

    #1. Asegúrate de tener Java y PySpark instalados:
    #pip install pyspark

    #2. Ejecuta el script con spark-submit y la dependencia de Kafka:

    #spark-submit \
    #    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 \
    #   streaming/pyspark_streaming.py

    #Nota: Ajusta la versión de spark-sql-kafka y Spark a la que tengas instalada.

    import json
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import from_json, col
    from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

    # 1. Definir el esquema de datos
    # -----------------------------------------------------------
    # Este esquema describe la estructura JSON que recibimos del tópico de Kafka.
    # Cada campo coincide con lo generado por el simulador iot_data_simulator.py.

    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("sensor_id", IntegerType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("vibration", DoubleType(), True),
        StructField("pressure", DoubleType(), True),
        StructField("voltage", DoubleType(), True)
    ])

    # 2. Crear la sesión de Spark
    # -----------------------------------------------------------
    # Usamos builder para configurar la aplicación Spark.

    spark = (
        SparkSession.builder
            .appName("IoTStreamProcessor")
            .getOrCreate()
    )

    # 3. Configurar la lectura desde Kafka
    # -----------------------------------------------------------
    # "subscribe" indica el tópico de Kafka que escuchamos.
    # "startingOffsets" = "latest" para leer solo nuevos datos.

    kafka_df = (
        spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "iot_sensor_data")
        .option("startingOffsets", "latest")
        .load()
    )

    # 4. Extraer y parsear el valor JSON
    # -----------------------------------------------------------
    # Kafka retorna la columna "value" en binario. Convertimos a string,
    # luego usamos from_json con nuestro esquema definido.

    json_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("jsonData")
    )

    # 5. Seleccionar campos individuales
    # -----------------------------------------------------------
    # Extraemos cada atributo de la columna "jsonData".

    sensor_data_df = json_df.select(
        col("jsonData.timestamp").alias("timestamp"),
        col("jsonData.sensor_id").alias("sensor_id"),
        col("jsonData.temperature").alias("temperature"),
        col("jsonData.vibration").alias("vibration"),
        col("jsonData.pressure").alias("pressure"),
        col("jsonData.voltage").alias("voltage")
    )

    # 6. Lógica de procesamiento
    # -----------------------------------------------------------
    # Aquí es donde podríamos realizar filtros, agregaciones, etc.
    # En este ejemplo, solo mostramos los registros por consola.

    # Ejemplo: Filtrar datos de temperatura excesiva (opcional)
    # sensor_data_df = sensor_data_df.filter(col("temperature") > 80)

    # 7. Escribir el resultado en la consola
    # -----------------------------------------------------------
    # outputMode = "append" para transmitir nuevos registros conforme llegan.

    query = (
        sensor_data_df
        .writeStream
        .outputMode("append")
        .format("console")
        .option("truncate", "false")
        .start()
    )

    # 8. Esperar indefinidamente
    # -----------------------------------------------------------
    # Para mantener la aplicación en ejecución en busca de eventos.

    query.awaitTermination()

"""