import socket

def autenticar_identidad(clave):
    with open("base_datos.txt", "r") as archivo:
        lineas = archivo.readlines()
        for i in range(0, len(lineas), 2):
            if lineas[i].strip() == clave:
                return True
    return False

def handle_cliente_servidor_b(cliente):
    while True:
        data = cliente.recv(1024).decode()
        if not data:
            break
        
        # Procesar solicitud del cliente
        comando, *parametros = data.split()
        
        if comando == "AUTENTICAR_IDENTIDAD":
            clave = parametros[0]
            if autenticar_identidad(clave):
                cliente.send(b"VALIDA\n")
            else:
                cliente.send(b"INVALIDA\n")
        
        else:
            cliente.send(b"Comando no reconocido\n")
    
    cliente.close()

def iniciar_servidor_b():
    host = "localhost"
    port = 5001
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen(1)
    
    print("Servidor B iniciado en {}:{}".format(host, port))
    
    while True:
        cliente, direccion = servidor.accept()
        print("Cliente conectado desde:", direccion)
        handle_cliente_servidor_b(cliente)

iniciar_servidor_b()
