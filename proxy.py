import socket

def redirigir_consulta(proxy, servidor, consulta):
    servidor.send(consulta.encode())
    respuesta = servidor.recv(1024).decode()
    proxy.send(respuesta.encode())

def handle_cliente(proxy, servidor_a, servidor_b):
    while True:
        data = proxy.recv(1024).decode()
        if not data:
            break

        comando, *parametros = data.split()

        if comando == "REGISTRAR_USUARIO":
            # Redirigir consulta al servidor A
            redirigir_consulta(proxy, servidor_a, data)

        elif comando == "SOLICITAR_CLAVE":
            # Redirigir consulta al servidor A y recibir respuesta
            servidor_a.send(data.encode())
            respuesta_a = servidor_a.recv(1024).decode()

            if respuesta_a.startswith("Clave no encontrada"):
                # Redirigir consulta al servidor B y recibir respuesta
                servidor_b.send(data.encode())
                respuesta_b = servidor_b.recv(1024).decode()
                proxy.send(respuesta_b.encode())
            else:
                proxy.send(respuesta_a.encode())

        elif comando == "AUTENTICAR_IDENTIDAD":
            # Redirigir consulta al servidor B y recibir respuesta
            print("mm")
            redirigir_consulta(proxy, servidor_b, data)

        else:
            proxy.send(b"Comando no reconocido\n")

    proxy.close()

def proxy():
    host = "localhost"
    puerto_proxy = 6000
    puerto_servidor_a = 5000
    puerto_servidor_b = 5001

    servidor_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_a.connect((host, puerto_servidor_a))

    servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_b.connect((host, puerto_servidor_b))

    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((host, puerto_proxy))
    proxy.listen(1)

    print("Proxy iniciado en {}:{}".format(host, puerto_proxy))
    print("Conexión establecida con Servidor A en {}:{}".format(host, puerto_servidor_a))
    print("Conexión establecida con Servidor B en {}:{}".format(host, puerto_servidor_b))

    while True:
        cliente, direccion = proxy.accept()
        print("Cliente conectado desde:", direccion)
        handle_cliente(cliente, servidor_a, servidor_b)

    proxy.close()
    servidor_a.close()
    servidor_b.close()

if __name__ == "__main__":
    proxy()