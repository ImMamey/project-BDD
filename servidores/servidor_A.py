import os
import socket
import random
import hashlib
import sqlite3
#TODO: si se desea correr local, hay que borrar la direccion local del volumen
def generar_clave():
    """
    Genera una clave aleatoria de 8 dígitos.

    Returns:
        str: Clave generada.
    """
    return str(random.randint(10000000, 99999999))

def registrar_usuario(cedula, nombre, clave):
    """
    Registra un nuevo usuario en la base de datos.

    Args:
        cedula (str): Cédula del usuario.
        nombre (str): Nombre del usuario.
        clave (str): Clave del usuario.

    Returns:
        str: Respuesta del registro.
    """
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE cedula = ?", (cedula,))
    resultado = cursor.fetchone()

    if resultado:
        clave_registrada = resultado[1]
        respuesta = f"Ya estás registrado. Tu clave es: {clave_registrada}"
    else:
        cursor.execute("INSERT INTO usuarios (cedula, clave, nombre) VALUES (?, ?, ?)", (cedula, clave, nombre))
        conn.commit()
        respuesta = f"Usuario registrado. Tu clave es: {clave}"

    conn.close()
    return respuesta

def solicitar_clave(identidad):
    """
    Obtiene la clave de un usuario registrado.

    Args:
        identidad (str): Identidad del usuario (nombre).

    Returns:
        str: Clave del usuario si existe, None si no existe.
    """
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    cursor.execute("SELECT clave FROM usuarios WHERE nombre = ?", (identidad,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]
    else:
        return None

def handle_cliente_servidor_a(cliente):
    """
    Maneja las solicitudes de un cliente al servidor A.

    Args:
        cliente (socket): Socket del cliente conectado.
    """
    while True:
        data = cliente.recv(1024).decode()
        if not data:
            break

        comando, *parametros = data.split()

        if comando == "REGISTRAR_USUARIO":
            cedula, nombre = parametros
            clave = generar_clave()
            respuesta = registrar_usuario(cedula, nombre, clave)
            cliente.send(respuesta.encode())

        elif comando == "SOLICITAR_CLAVE":
            identidad = parametros[0]
            clave = solicitar_clave(identidad)

            if clave:
                cliente.send(clave.encode())
            else:
                cliente.send(b"Clave no encontrada\n")
        else:
            cliente.send(b"Comando no reconocido\n")

    cliente.close()

def iniciar_servidor_a():
    host = "0.0.0.0"
    port = 5000

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen(1)

    print("Servidor A iniciado en {}:{}".format(host, port))

    while True:
        cliente, direccion = servidor.accept()
        print("Cliente conectado desde:", direccion)
        handle_cliente_servidor_a(cliente)

if __name__ == "__main__":
    if os.environ.get("APP_IN_DOCKER") is not None:
        sqlite_path="/data/usuarios.db"
    else:
        sqlite_path="usuarios.db"

    iniciar_servidor_a()
