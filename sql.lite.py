import sqlite3
import hashlib
import csv
# Función para convertir una cadena en MD5
def convertir_md5(cadena):
    md5_hash = hashlib.md5()
    md5_hash.update(cadena.encode('utf-8'))
    return md5_hash.hexdigest()

# Conexión a la base de datos
conn = sqlite3.connect('servidores/usuarios.db')
cursor = conn.cursor()

# Crear la tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                  (cedula INTEGER PRIMARY KEY,
                   clave TEXT,
                   nombre TEXT)''')

cursor.execute('''SELECT * from usuarios''')
rows = cursor.fetchall()

# Mostrar los resultados
for row in rows:
    print(row)

# Ruta del archivo de salida CSV
ruta_archivo_csv = './Datos.txt'  # Actualiza con la ruta deseada

# Exportar los datos a un archivo CSV
with open(ruta_archivo_csv, 'w', newline='') as archivo_csv:
    csv_writer = csv.writer(archivo_csv)
    csv_writer.writerow([i[0] for i in cursor.description])  # Escribir encabezados de columna
    csv_writer.writerows(rows)  # Escribir filas de datos


conn.commit()
conn.close()