import socket
import hashlib
import sqlite3
import random

def generar_nueva_clave():
    clave = ""
    for _ in range(8):
        digito = random.randint(0, 9)
        clave += str(digito)
    return clave

def generar_clave(conn, cliente_socket):
    cursor = conn.cursor()

    # Recibir nombre de usuario del cliente
    nombre_usuario = cliente_socket.recv(1024).decode()

    # Verificar si el nombre de usuario ya existe en la base de datos
    cursor.execute("SELECT clave FROM usuarios WHERE identidad = ?", (nombre_usuario,))
    resultado = cursor.fetchone()

    if resultado:
        # El nombre de usuario ya existe, obtener la clave asociada
        clave = resultado[0]
        return clave
    else:
        # El nombre de usuario no existe, generar una nueva clave
        nueva_clave = generar_nueva_clave()

        # Insertar el nuevo nombre de usuario y clave en la base de datos
        cursor.execute("INSERT INTO usuarios (clave, identidad) VALUES (?, ?)", (nueva_clave, nombre_usuario))
        conn.commit()

        return nueva_clave

def autenticar_identidad(conn, identidad):
    cursor = conn.cursor()
    
    # Verificar si la identidad existe en la base de datos
    cursor.execute("SELECT id FROM usuarios WHERE identidad = ?", (identidad,))
    resultado = cursor.fetchone()
    
    if resultado:
        return "VALIDA"
    else:
        return "INVALIDA"

def servidor_a():
    host = "localhost"
    puerto = 5000

    conn = sqlite3.connect('usuarios.db')

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(1)

    print("Servidor A de Claves iniciado. Esperando conexiones...")

    while True:
        cliente, direccion = servidor.accept()
        print("Cliente conectado:", direccion)

        # Generar o recuperar clave asociada al nombre de usuario del cliente
        clave = generar_clave(conn, cliente)

        # Enviar clave al cliente
        cliente.send(clave.encode())

        cliente.close()

    conn.close()

servidor_a()