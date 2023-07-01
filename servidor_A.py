import socket
import random
import hashlib
import sqlite3


def generar_clave():
    return str(random.randint(10000000, 99999999))


def registrar_usuario(cedula, nombre, clave):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Verificar si el usuario ya está registrado
    cursor.execute("SELECT * FROM usuarios WHERE cedula = ?", (cedula,))
    resultado = cursor.fetchone()

    if resultado:
        # Usuario ya registrado
        clave_registrada = resultado[1]
        respuesta = f"Ya estás registrado. Tu clave es: {clave_registrada}"
    else:
        # Usuario nuevo
        cursor.execute("INSERT INTO usuarios (cedula, clave, nombre) VALUES (?, ?, ?)", (cedula, clave, nombre))
        conn.commit()
        respuesta = f"Usuario registrado. Tu clave es: {clave}"

    conn.close()
    return respuesta


def handle_cliente_servidor_a(cliente):
    while True:
        data = cliente.recv(1024).decode()
        if not data:
            break

        # Procesar solicitud del cliente
        comando, *parametros = data.split()

        if comando == "REGISTRAR_USUARIO":
            cedula, nombre = parametros
            clave = generar_clave()
            respuesta = registrar_usuario(cedula, nombre, clave)
            cliente.send(respuesta.encode())

        elif comando == "FIRMAR_MENSAJE":
            identidad, mensaje = parametros
            # Lógica para firmar el mensaje con la identidad y el mensaje

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


iniciar_servidor_a()