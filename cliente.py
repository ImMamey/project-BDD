import socket
import hashlib
import base64
from Crypto.Cipher import AES


def solicitar_clave(servidor_a, identidad):
    servidor_a.send(("SOLICITAR_CLAVE " + identidad).encode())
    clave = servidor_a.recv(1024).decode()
    return clave


def registrar_usuario(servidor_a):
    print("=== Registro de Usuario ===")
    cedula = input("Ingrese su cédula: ")
    nombre = input("Ingrese su nombre: ")

    servidor_a.send(("REGISTRAR_USUARIO {} {}".format(cedula, nombre)).encode())
    respuesta = servidor_a.recv(1024).decode().strip()

    print(respuesta)


def procesar_archivo_entrada(servidor_a, identidad2):
    with open("entrada.txt", "r") as archivo_entrada:
        tipo_operacion = archivo_entrada.readline().strip()
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()

    if tipo_operacion == "FIRMAR":
        clave = solicitar_clave(servidor_a, identidad2)
        if clave:
            hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
            firma = cifrar_hash(hash_md5, clave)
            resultado = f"{clave}\n{firma}\n0"
            guardar_resultado(resultado)
            print("Firma generada y guardada en salida.txt")
        else:
            print("No se pudo obtener la clave del servidor A")
    elif tipo_operacion == "AUTENTICAR":
        respuesta = 0
        return respuesta
    elif tipo_operacion == "INTEGRIDAD":
        resultado = 0
        return resultado


def guardar_resultado(resultado):
    with open("salida.txt", "w") as archivo_salida:
        archivo_salida.write(resultado)


def cifrar_hash(hash_md5, clave):
    print(clave)
    clave = clave.ljust(32)[:32]  # Asegurarse de que la clave tenga 32 bytes
    cifrador = AES.new(clave.encode(), AES.MODE_ECB)
    hash_bytes = hash_md5.encode()
    longitud_relleno = 16 - (len(hash_bytes) % 16)
    hash_relleno = hash_bytes + bytes([longitud_relleno] * longitud_relleno)
    hash_cifrado = cifrador.encrypt(hash_relleno)
    hash_cifrado_base64 = base64.b64encode(hash_cifrado).decode()
    return hash_cifrado_base64


def cliente():
    host = "localhost"
    puerto_a = 5000
    puerto_b = 5001

    servidor_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor_a.connect((host, puerto_a))
    servidor_b.connect((host, puerto_b))

    print("=== Menú Principal ===")
    print("1. Registrarse")
    print("2. Firmar Mensaje")
    print("3. Autenticar Identidad")
    print("4. Verificar Integridad")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_usuario(servidor_a)
    elif opcion == "2":
        identidad = input("Ingrese su nombre: ")
        procesar_archivo_entrada(servidor_a, identidad)
    elif opcion == "3":
        print("Opción no válida.")
    elif opcion == "4":
        print("Opción no válida.")
    else:
        print("Opción no reconocida.")

    servidor_a.close()
    servidor_b.close()


if __name__ == "__main__":
    cliente()
