import socket
import random

def generar_clave():
    # Generar una clave numérica de 8 dígitos
    clave = str(random.randint(10000000, 99999999))
    return clave

def guardar_clave(identidad, clave):
    with open("base_datos.txt", "a") as archivo:
        archivo.write(clave + "\n")
        archivo.write(identidad + "\n")

def handle_cliente_servidor_a(cliente):
    while True:
        data = cliente.recv(1024).decode()
        if not data:
            break
        
        # Procesar solicitud del cliente
        comando, *parametros = data.split()
        
        if comando == "SOLICITAR_CLAVE":
            identidad = parametros[0]
            clave = generar_clave()
            guardar_clave(identidad, clave)
            # Envía la clave generada al cliente
            cliente.send(clave.encode())
        
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

