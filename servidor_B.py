import socket
import sqlite3

def autenticar_identidad(clave):
    # Conexión a la base de datos
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Ejecutar consulta SQL para verificar la identidad del usuario
    cursor.execute("SELECT nombre FROM usuarios WHERE clave=?", (clave,))
    resultado = cursor.fetchone()

    if resultado:
        nombre = resultado[0]
        respuesta = "USUARIO_EXISTE " + nombre
    else:
        respuesta = "USUARIO_NO_EXISTE"

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    return respuesta

def servidor_b():
    host = "localhost"
    puerto_b = 5001

    servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_b.bind((host, puerto_b))
    servidor_b.listen(1)

    print("Servidor B en espera de conexiones...")

    while True:
        conn, addr = servidor_b.accept()
        print("Cliente conectado:", addr)

        opcion = conn.recv(1024).decode()
        if opcion.startswith("AUTENTICAR_IDENTIDAD"):
            clave = opcion.split()[1]
            respuesta = autenticar_identidad(clave)
            conn.send(respuesta.encode())

        conn.close()


if __name__ == "__main__":
    servidor_b()
