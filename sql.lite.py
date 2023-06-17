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
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   clave TEXT,
                   identidad TEXT)''')

# Ejemplo de inserción de datos con clave en formato MD5
clave = '12345678'
clave_md5 = convertir_md5(clave)
identidad = 'usuario1'
cursor.execute("INSERT INTO usuarios (clave, identidad) VALUES (?, ?)", (clave_md5, identidad))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()