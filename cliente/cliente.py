import os
import socket
import hashlib
import base64
from Crypto.Cipher import AES

def solicitar_clave(proxy, identidad):
    """
    Envía una solicitud al servidor proxy para obtener la clave asociada a una identidad.

    Args:
        proxy (socket): Socket del cliente para la comunicación con el servidor proxy.
        identidad (str): Identidad para la cual se solicita la clave.

    Returns:
        str: Clave asociada a la identidad.
    """
    proxy.send(("SOLICITAR_CLAVE " + identidad).encode())
    clave = proxy.recv(1024).decode()
    return clave

def registrar_usuario(proxy):
    """
    Registra un nuevo usuario enviando los datos al servidor proxy.

    Args:
        proxy (socket): Socket del cliente para la comunicación con el servidor proxy.
    """
    print("=== Registro de Usuario ===")
    cedula = input("Ingrese su cédula: ")
    nombre = input("Ingrese su nombre: ")

    proxy.send(("REGISTRAR_USUARIO {} {}".format(cedula, nombre)).encode())
    respuesta = proxy.recv(1024).decode().strip()

    print(respuesta)

def crear_archivo_entrada(resultado):
    """
    Crea un archivo de entrada y guarda un resultado en él.

    Args:
        resultado (str): Resultado a guardar en el archivo de entrada.
    """
    with open(entrada_path, "w") as archivo_salida:
        archivo_salida.write(resultado)

def procesar_archivo_entrada(proxy, identidad):
    """
    Procesa el archivo de entrada, obteniendo el mensaje, generando una firma y guardando el resultado en un archivo.

    Args:
        proxy (socket): Socket del cliente para la comunicación con el servidor proxy.
        identidad (str): Identidad del usuario.
    """
    with open(entrada_path, "r") as archivo_entrada:
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
    """
    Obtiene el hash MD5 del mensaje del archivo de entrada.

    Returns:
        str: Hash MD5 del mensaje.
    """
    with open(entrada_path, "r") as archivo_entrada:
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()
        hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
        return hash_md5

def descifrar_mensaje():
    """
    Descifra el mensaje guardado en el archivo de salida y verifica su integridad.
    """
    with open(salida_path, "r") as archivo_salida:
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
    """
    Elimina el relleno aplicado a los datos.

    Args:
        datos (bytes): Datos a los cuales se les aplicó relleno.

    Returns:
        bytes: Datos sin relleno.
    """
    longitud_relleno = datos[-1]
    return datos[:-longitud_relleno]

def guardar_resultado(resultado):
    """
    Guarda el resultado en el archivo de salida.

    Args:
        resultado (str): Resultado a guardar en el archivo de salida.
    """
    with open(salida_path, "w") as archivo_salida:
        archivo_salida.write(resultado)

def cifrar_hash(hash_md5, clave):
    """
    Cifra el hash MD5 utilizando una clave.

    Args:
        hash_md5 (str): Hash MD5 a cifrar.
        clave (str): Clave utilizada para el cifrado.

    Returns:
        str: Hash MD5 cifrado y convertido a Base64.
    """
    clave = clave.ljust(32)[:32]
    cifrador = AES.new(clave.encode(), AES.MODE_ECB)
    datos_rellenados = rellenar_datos(hash_md5.encode())
    datos_cifrados = cifrador.encrypt(datos_rellenados)
    firma_base64 = base64.b64encode(datos_cifrados).decode()
    return firma_base64

def rellenar_datos(datos):
    """
    Rellena los datos para que tengan una longitud múltiplo de 16.

    Args:
        datos (bytes): Datos a rellenar.

    Returns:
        bytes: Datos rellenados.
    """
    longitud_relleno = 16 - (len(datos) % 16)
    datos_rellenados = datos + bytes([longitud_relleno]) * longitud_relleno
    return datos_rellenados

def autenticar_identidad(proxy):
    """
    Autentica la identidad del usuario enviando la clave al servidor proxy.

    Args:
        proxy (socket): Socket del cliente para la comunicación con el servidor proxy.
    """
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
    """
    Muestra el menú principal y solicita al usuario que seleccione una opción.

    Returns:
        str: Opción seleccionada por el usuario.
    """
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
    """
    Función principal del cliente que establece la conexión con el servidor proxy y maneja las opciones del menú.
    """
    host = os.environ.get("HOST_PROXY", "127.0.0.1")
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
    if os.environ.get("APP_IN_DOCKER") is not None:
        entrada_path="/data/entrada.txt"
        salida_path="/data/salida.txt"
    else:
        entrada_path="entrada.txt"
        salida_path="salida.txt"
    cliente()
