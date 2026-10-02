import os
import pymysql
from pymysql.cursors import DictCursor

# Configuración de tu servidor MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '12345'  # Si usas XAMPP suele ir vacío; si usas instalador de MySQL coloca tu clave
MYSQL_DB = 'cauchoscoca_db'
MYSQL_PORT = 3306

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_PATH = os.path.join(BASE_DIR, 'sql', 'esquema.sql')

def get_db_connection():
    """Establece conexión a MySQL y retorna registros en formato diccionario."""
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
        cursorclass=DictCursor,
        autocommit=True
    )

def init_db():
    """Ejecuta el script SQL para crear la estructura de tablas."""
    if os.path.exists(SQL_PATH):
        conn = get_db_connection()
        cursor = conn.cursor()
        with open(SQL_PATH, 'r', encoding='utf-8') as f:
            statements = f.read().split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
        cursor.close()
        conn.close()
        print("Base de datos MySQL inicializada correctamente.")
    else:
        print(f"Advertencia: No se encontró el archivo {SQL_PATH}")

if __name__ == '__main__':
    init_db()