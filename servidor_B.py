import socket
import sqlite3

def autenticar_identidad(conn, cliente_socket, clave):
    cursor = conn.cursor()

    # Verificar la existencia de la clave en la base de datos
    cursor.execute("SELECT clave FROM usuarios WHERE clave = ?", (clave,))
    resultado = cursor.fetchone()

    if resultado:
        respuesta = "VALIDA"
    else:
        respuesta = "INVALIDA"

    # Enviar la respuesta al cliente
    cliente_socket.send(respuesta.encode())

def servidor_b():
    host = "localhost"
    puerto = 5001

    # Conexión a la base de datos
    conn = sqlite3.connect('usuarios.db')

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(1)

    print("Servidor B en espera de conexiones...")

    while True:
        cliente_socket, cliente_direccion = servidor.accept()
        print(f"Cliente conectado: {cliente_direccion}")

        # Recibir la clave del cliente
        clave = cliente_socket.recv(1024).decode()

        # Autenticar la clave en la base de datos
        autenticar_identidad(conn, cliente_socket, clave)

        cliente_socket.close()

    # Cerrar la conexión a la base de datos
    conn.close()

servidor_b()