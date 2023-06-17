import socket

def solicitar_clave(servidor_a, identidad):
    # Enviar solicitud de clave al Servidor A
    servidor_a.send(("SOLICITAR_CLAVE " + identidad).encode())
    clave = servidor_a.recv(1024).decode()
    return clave

def autenticar_identidad(servidor_b, clave):
    # Enviar solicitud de autenticación al Servidor B
    servidor_b.send(("AUTENTICAR_IDENTIDAD " + clave).encode())
    respuesta = servidor_b.recv(1024).decode()
    if respuesta == "VALIDA":
        return True
    else:
        return False

def firmar_mensaje(servidor_a, clave, mensaje):
    # Enviar solicitud de firma al Servidor A
    servidor_a.send(("FIRMAR " + clave + " " + mensaje).encode())
    firma = servidor_a.recv(1024).decode()
    return firma

def verificar_integridad(servidor_a, firma, mensaje):
    # Enviar solicitud de verificación al Servidor A
    servidor_a.send(("VERIFICAR " + firma + " " + mensaje).encode())
    respuesta = servidor_a.recv(1024).decode()
    if respuesta == "INTEGRO":
        return True
    else:
        return False

def conectar_servidores():
    host_a = "localhost"
    port_a = 5000
    
    host_b = "localhost"
    port_b = 5001
    
    servidor_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    servidor_a.connect((host_a, port_a))
    servidor_b.connect((host_b, port_b))
    
    while True:
        comando = input("Ingrese el comando (AUTENTICAR, FIRMAR, VERIFICAR): ")
        
        if comando == "AUTENTICAR":
            clave = input("Ingrese la clave: ")
            if autenticar_identidad(servidor_b, clave):
                print("La identidad es válida.")
            else:
                print("La identidad es inválida.")
        
        elif comando == "FIRMAR":
            clave = input("Ingrese la clave: ")
            mensaje = input("Ingrese el mensaje: ")
            firma = firmar_mensaje(servidor_a, clave, mensaje)
            print("La firma electrónica generada es:", firma)
        
        elif comando == "VERIFICAR":
            firma = input("Ingrese la firma electrónica: ")
            mensaje = input("Ingrese el mensaje: ")
            if verificar_integridad(servidor_a, firma, mensaje):
                print("El mensaje es íntegro.")
            else:
                print("El mensaje ha sido alterado.")
        
        else:
            print("Comando no reconocido.")
    
    servidor_a.close()
    servidor_b.close()

conectar_servidores()
