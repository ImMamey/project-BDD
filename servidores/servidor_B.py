import socket
import sqlite3

def autenticar_identidad(clave):
    """
    Verifica la identidad de un usuario.

    Args:
        clave (str): Clave del usuario.

    Returns:
        str: Respuesta de la autenticación.
    """
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

def handle_cliente_servidor_b(cliente):
    """
    Maneja las solicitudes de un cliente al servidor B.

    Args:
        cliente (socket): Socket del cliente conectado.
    """
    while True:
        data = cliente.recv(1024).decode()
        if not data:
            break

        opcion, clave = data.split()
        if opcion == "AUTENTICAR_IDENTIDAD":
            respuesta = autenticar_identidad(clave)
            cliente.send(respuesta.encode())

    cliente.close()

def iniciar_servidor_b():
    host = "localhost"
    puerto_b = 5001

    servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_b.bind((host, puerto_b))
    servidor_b.listen(1)

    print("Servidor B en espera de conexiones...")

    while True:
        conn, addr = servidor_b.accept()
        print("Cliente conectado:", addr)
        handle_cliente_servidor_b(conn)

if __name__ == "__main__":
    iniciar_servidor_b()
