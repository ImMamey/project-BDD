import socket
import hashlib
import base64
from Crypto.Cipher import AES

def solicitar_clave(proxy, identidad):
    proxy.send(("SOLICITAR_CLAVE " + identidad).encode())
    clave = proxy.recv(1024).decode()
    return clave

def registrar_usuario(proxy):
    print("=== Registro de Usuario ===")
    cedula = input("Ingrese su cédula: ")
    nombre = input("Ingrese su nombre: ")

    proxy.send(("REGISTRAR_USUARIO {} {}".format(cedula, nombre)).encode())
    respuesta = proxy.recv(1024).decode().strip()

    print(respuesta)

def crear_archivo_entrada(resultado):
    with open("entrada.txt", "w") as archivo_salida:
        archivo_salida.write(resultado)

def procesar_archivo_entrada(proxy, identidad):
    with open("entrada.txt", "r") as archivo_entrada:
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()
        try:
            clave = solicitar_clave(proxy, identidad)
            if clave != "Clave no encontrada\n":
                hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
                firma = cifrar_hash(hash_md5, clave)
                resultado = f"{clave}\n{firma}\n{mensaje}\n0"
                guardar_resultado(resultado)
                print("Firma generada y guardada en salida.txt")
            else:
                print("No se pudo obtener la clave del servidor")
        except:
            print("Error al cifrar, el usuario no existe.")

def obtener_hash_entrada():
    with open("entrada.txt", "r") as archivo_entrada:
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()
        hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
        return hash_md5

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
            hash_entrada = obtener_hash_entrada()
            hash_md5_calculado = hashlib.md5(mensaje.encode()).hexdigest()
            print("hash_MD5 entrada", hash_entrada)
            print("Bloque Hash calculado:", hash_md5_calculado)
            if hash_MD5_original == hash_md5_calculado and hash_entrada == hash_md5_calculado:
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
    datos_rellenados = rellenar_datos(hash_md5.encode())
    datos_cifrados = cifrador.encrypt(datos_rellenados)
    firma_base64 = base64.b64encode(datos_cifrados).decode()
    return firma_base64

def rellenar_datos(datos):
    longitud_relleno = 16 - (len(datos) % 16)
    datos_rellenados = datos + bytes([longitud_relleno]) * longitud_relleno
    return datos_rellenados

def autenticar_identidad(proxy):
    clave = input("Ingrese la clave del usuario: ")
    proxy.send(("AUTENTICAR_IDENTIDAD " + clave).encode())
    respuesta = proxy.recv(1024).decode()
    if respuesta.startswith("USUARIO_EXISTE"):
        nombre = respuesta.split()[1]
        print("El firmante existe.")
        print("Nombre: ", nombre)
        print("Clave: ", clave)
    else:
        print("El usuario no existe.")


def menu():
    print("=== Menú Principal ===")
    print("1. Registrar Usuario")
    print("2. Procesar Archivo de Entrada")
    print("3. Verificar Mensaje Descifrado")
    print("4. Autenticar Identidad")
    print("5. Salir")

    while True:
        opcion = input("Seleccione una opción: ")
        if opcion in ["1", "2", "3", "4", "5"]:
            return opcion
        else:
            print("Opción inválida. Intente nuevamente.")

def cliente():
    host = "localhost"
    puerto_proxy = 6000

    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.connect((host, puerto_proxy))

    while True:
        opcion = menu()

        if opcion == "1":
            registrar_usuario(proxy)
        elif opcion == "2":
            identidad = input("Ingrese su nombre: ")
            mensaje = input("Ingrese su mensaje: ")
            resultado = f"{identidad}\n{mensaje}\n0"
            crear_archivo_entrada(resultado)
            procesar_archivo_entrada(proxy, identidad)
        elif opcion == "3":
            descifrar_mensaje()
        elif opcion == "4":
            autenticar_identidad(proxy)
        elif opcion == "5":
            break
    proxy.close()

if __name__ == "__main__":
    cliente()
