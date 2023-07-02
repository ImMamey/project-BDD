import socket
import random
import hashlib
import sqlite3

def generar_clave():
    return str(random.randint(10000000, 99999999))

def registrar_usuario(cedula, nombre, clave):
    conn = sqlite3.connect('usuarios.db')
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
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute("SELECT clave FROM usuarios WHERE nombre = ?", (identidad,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]
    else:
        return None

def handle_cliente_servidor_a(cliente):
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
    host = "localhost"
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
    iniciar_servidor_a()
