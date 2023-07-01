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
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()
        try:
            clave = solicitar_clave(servidor_a, identidad2)
            if clave:
                hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
                firma = cifrar_hash(hash_md5, clave)
                resultado = f"{clave}\n{firma}\n{mensaje}\n0"
                guardar_resultado(resultado)
                print("Firma generada y guardada en salida.txt")
            else:
                print("No se pudo obtener la clave del servidor A")
        except:
            print("error al cifrar")


def descifrar_mensaje():
    with open("salida.txt", "r") as archivo_salida:
        clave = archivo_salida.readline().strip()
        firma = archivo_salida.readline().strip()
        mensaje = archivo_salida.readline().strip()
        final = archivo_salida.readline().strip()
        try:
            clave = clave.ljust(32)[:32]
            cifrador = AES.new(clave.encode(), AES.MODE_ECB)
            mensaje_bytes = base64.b64decode(firma)
            MD5_descifrado = cifrador.decrypt(mensaje_bytes)
            MD5_descifrado = eliminar_relleno(MD5_descifrado)
            hash_MD5_original = MD5_descifrado.decode()
            print("este es la clave:", clave)
            print("este es el mensaje recibido:", mensaje)

            print("hash_MD5 original", hash_MD5_original)

            hash_md5_calculado = hashlib.md5(mensaje.encode()).hexdigest()
            print("Bloque Hash calculado:", hash_md5_calculado)

            if hash_MD5_original == hash_md5_calculado:
                print("El mensaje es íntegro. Bloques Hash coinciden.")
            else:
                print("El mensaje no es íntegro. Bloques Hash no coinciden.")
        except:
            print("Error al descifrar el mensaje")


def eliminar_relleno(datos):
    longitud_relleno = datos[-1]
    return datos[:-longitud_relleno]


def guardar_resultado(resultado):
    with open("salida.txt", "w") as archivo_salida:
        archivo_salida.write(resultado)


def cifrar_hash(hash_md5, clave):
    clave = clave.ljust(32)[:32]
    cifrador = AES.new(clave.encode(), AES.MODE_ECB)
    hash_bytes = hash_md5.encode()
    longitud_relleno = 16 - (len(hash_bytes) % 16)
    hash_relleno = hash_bytes + bytes([longitud_relleno] * longitud_relleno)
    hash_cifrado = cifrador.encrypt(hash_relleno)
    hash_cifrado_base64 = base64.b64encode(hash_cifrado).decode()
    return hash_cifrado_base64

def autenticar_identidad(servidor_b):
    clave = input("Ingrese la clave del usuario: ")
    servidor_b.send(("AUTENTICAR_IDENTIDAD " + clave).encode())
    respuesta = servidor_b.recv(1024).decode()
    if respuesta.startswith("USUARIO_EXISTE"):
        nombre = respuesta.split()[1]
        print("EL firmante existe.")
        print("Nombre: ", nombre)
        print("Clave: ", clave)
    else:
        print("El usuario no existe.")


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
    print("3. Descifrar Mensaje")
    print("4. Autenticar Identidad")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_usuario(servidor_a)
    elif opcion == "2":
        identidad = input("Ingrese su nombre: ")
        procesar_archivo_entrada(servidor_a, identidad)
    elif opcion == "3":
        descifrar_mensaje()
    elif opcion == "4":
        autenticar_identidad(servidor_b)
    else:
        print("Opción no reconocida.")

    servidor_a.close()
    servidor_b.close()


if __name__ == "__main__":
    cliente()