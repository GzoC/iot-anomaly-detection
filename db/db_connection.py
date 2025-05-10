# db/db_connection.py
# -*- coding: utf-8 -*-
"""
Módulo para crear conexión a PostgreSQL con SQLAlchemy.

Creado por Gonzalo Cisterna Salinas - github.com/GzoC
"""

from sqlalchemy import create_engine
import os

# Configuración de acceso a la base de datos
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "iotdb")

def get_engine():
    """
    Retorna un motor de conexión SQLAlchemy para PostgreSQL.
    """
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)
