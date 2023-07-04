import os
import sqlite3
import hashlib
import csv
# Función para convertir una cadena en MD5

if os.environ.get("APP_IN_DOCKER") is not None:
    db_path = "/data/usuarios.db"
else:
    db_path = "usuarios.db"

# Conexión a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear la tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                  (cedula INTEGER PRIMARY KEY,
                   clave TEXT,
                   nombre TEXT)''')


conn.commit()
conn.close()