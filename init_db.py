import os
import sqlite3

def crear_base_de_datos():
    # 1. Asegurar que la carpeta 'data' exista
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Carpeta 'data/' creada correctamente.")

    # 2. Conectar (esto creará el archivo 'cauchoscoca.db' si no existe)
    ruta_db = os.path.join('data', 'cauchoscoca.db')
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # 3. Crear la tabla 'productos' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Base de datos e infraestructura creadas exitosamente en: {ruta_db}")

if __name__ == '__main__':
    crear_base_de_datos()