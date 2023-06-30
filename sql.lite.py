import sqlite3
import hashlib

# Función para convertir una cadena en MD5
def convertir_md5(cadena):
    md5_hash = hashlib.md5()
    md5_hash.update(cadena.encode('utf-8'))
    return md5_hash.hexdigest()

# Conexión a la base de datos
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear la tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                  (cedula INTEGER PRIMARY KEY,
                   clave TEXT,
                   nombre TEXT)''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()