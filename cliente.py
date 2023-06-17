from Crypto.Cipher import AES
import socket
import hashlib
import base64

def cifrar_hash(hash_md5, clave):
    # Asegurarse de que la clave tenga 16, 24 o 32 bytes (128, 192 o 256 bits) para AES-128, AES-192 o AES-256 respectivamente
    clave = clave.ljust(32)[:32]  # Rellena con espacios y luego trunca a 32 bytes
    
    # Crear un objeto AES con la clave
    cifrador = AES.new(clave.encode(), AES.MODE_ECB)
    
    # Convertir el hash MD5 en bytes
    hash_bytes = hash_md5.encode()
    
    # Rellenar el hash para que tenga una longitud múltiplo de 16 bytes
    longitud_relleno = 16 - (len(hash_bytes) % 16)
    hash_relleno = hash_bytes + bytes([longitud_relleno] * longitud_relleno)
    
    # Cifrar el hash relleno
    hash_cifrado = cifrador.encrypt(hash_relleno)
    
    # Codificar el hash cifrado en base64 para obtener una representación legible
    hash_cifrado_base64 = base64.b64encode(hash_cifrado).decode()
    
    return hash_cifrado_base64

def firmar_mensaje(servidor_a, identidad, mensaje):
    # Enviar solicitud de clave al Servidor A
    servidor_a.send(("SOLICITAR_CLAVE " + identidad).encode())
    clave = servidor_a.recv(1024).decode()
    
    # Calcular el hash MD5 del mensaje
    hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
    
    # Cifrar el hash con la clave
    hash_cifrado = cifrar_hash(hash_md5, clave)
    
    # Devolver el texto de la firma del mensaje
    return hash_cifrado

def autenticar_identidad(servidor_b, clave):
    # Enviar solicitud de autenticación al Servidor B
    servidor_b.send(("AUTENTICAR_IDENTIDAD " + clave).encode())
    respuesta = servidor_b.recv(1024).decode().strip()
    
    return respuesta

def verificar_integridad(firma, mensaje):
    # Aquí implementa la lógica para descifrar la firma electrónica y comparar el bloque Hash con el del mensaje
    # Devolver "Mensaje INTEGRO" o "Mensaje NO INTEGRO"
    return 0

def procesar_archivo_entrada(servidor_a, servidor_b):
    with open("entrada.txt", "r") as archivo_entrada:
        tipo_operacion = archivo_entrada.readline().strip()
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()
    
    if tipo_operacion == "FIRMAR":
        return firmar_mensaje(servidor_a, identidad, mensaje)
    
    elif tipo_operacion == "AUTENTICAR":
        respuesta = autenticar_identidad(servidor_b, identidad)
        return respuesta
    
    elif tipo_operacion == "INTEGRIDAD":
        resultado = verificar_integridad(firma, mensaje)
        return resultado

def guardar_resultado(resultado):
    with open("salida.txt", "w") as archivo_salida:
        archivo_salida.write(resultado)

def cliente():
    host = "localhost"
    puerto_a = 8888
    puerto_b = 8889
    
    servidor_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    servidor_a.connect((host, puerto_a))
    servidor_b.connect((host, puerto_b))
    
    resultado = procesar_archivo_entrada(servidor_a, servidor_b)
    
    guardar_resultado(resultado)
    
    servidor_a.close()
    servidor_b.close()

cliente()