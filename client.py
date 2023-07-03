import socket
import re
import sys
import logging
import base64
import hashlib
from Crypto.Cipher import AES

LOG = logging.getLogger("Cliente")


class Client:
    """
    Contiene todos los metodos para el cliente.
    """

    def __init__(self, ip) -> None:
        """
        :var HEADER: Numero de bytes usado para algoritmo logico = como no sabemos cual es el tamaño de cada mensaje,
        todos los mensajes seran de 64 bytes. Facilita el encode/decode.
        :var PORT: Numero de puerto a usar.
        :var FORMAT: Formato de encode.
        :var DISCONNECT_MESSAGE: mensaje para la desconneción y cierre de sesion.
        :var SERVER: IP del servidor.
        :var ADDR: tupla con el IP del servidor y puerto del socket.

        """
        self.HEADER: int = 64
        self.PORT: int = 5555
        self.FORMAT: str = "utf-8"
        self.DISCONNECT_MESSAGE: str = "!DISCONNECT"
        self.SERVER: str = ip
        self.ADDR: tuple = (self.SERVER, self.PORT)
        LOG.info(f"[NUEVO CLIENTE] {self.ADDR} conectado.")

        self.start()

    def start(self) -> None:
        """
        Inicia el socket del cliente, se conectara a la tupla con los datos del servidor
        :return: None
        """
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
        except Exception as e:
            LOG.exception(
                "Error al tratarse de conectar al Proxy. "
                + "Por favor, cerrar el cliente y verificar la coneccion."
            )

    def send(self, msg) -> None:
        """
        Trata de enviar un mensaje al servidor. Si no devuelve un error.
        :param msg: Mensaje a enviar al servidor
        :return: None
        """
        try:
            message = msg.encode(self.FORMAT)  # encode el mensaje con el formato utf-8
            msg_length = len(message)  # calcula cantidad de caracteres en el mensaje
            send_length = str(msg_length).encode(
                self.FORMAT
            )  # chequea que los mensajes sean de 64bytes
            send_length += b" " * (self.HEADER - len(send_length))
            self.client.send(send_length)  # se envia los mensajes
            self.client.send(message)
            print(self.client.recv(2048).decode(self.FORMAT))
        except Exception as e:
            LOG.exception("Error al enviar el mensaje.")

# TODO: mover a #2 firmar mensaje dentro del proxy
def solicitar_clave(servidor_a, identidad):
    servidor_a.send(("SOLICITAR_CLAVE " + identidad).encode())
    clave = servidor_a.recv(1024).decode()
    return clave

def opcion_registrar_usuario() -> None:
    print("=== Registro de Usuario ===")
    cedula = input("\nIngrese su cédula:\n ")
    nombre = input("Ingrese su nombre:\n ")
    LOG.info(f"Cliente {cl.ADDR} solicitado Registrar un cliente.")
    msg = "[REGISTRAR] " + str(cedula) + " |!| " + str(nombre)
    cl.send(str(msg))

def cifrar_hash(hash_md5, clave):
    clave = clave.ljust(32)[:32]
    cifrador = AES.new(clave.encode(), AES.MODE_ECB)
    hash_bytes = hash_md5.encode()
    longitud_relleno = 16 - (len(hash_bytes) % 16)
    hash_relleno = hash_bytes + bytes([longitud_relleno] * longitud_relleno)
    hash_cifrado = cifrador.encrypt(hash_relleno)
    hash_cifrado_base64 = base64.b64encode(hash_cifrado).decode()
    return hash_cifrado_base64

def guardar_resultado(resultado):
    with open("salida.txt", "w") as archivo_salida:
        archivo_salida.write(resultado)

def crear_archivo_entrada(resultado):
    with open("entrada.txt", "w") as archivo_salida:
        #TODO: Borrar
        print("creando archivo con: ",resultado)
        archivo_salida.write(resultado)

def procesar_archivo_entrada(identidad2):
    with open("entrada.txt", "r") as archivo_entrada:
        identidad = archivo_entrada.readline().strip()
        mensaje = archivo_entrada.readline().strip()
        firma = archivo_entrada.readline().strip()
        try:
            msg = "[FIRMAR] " + str(identidad) + " |!| "
            cl.send(str(msg))

            #n = cl.client

            connected: bool = True
            while connected:
                msg_length = cl.client.recv(cl.HEADER).decode(cl.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    clave = cl.client.recv(msg_length).decode(cl.FORMAT)
                    connected = False
                    #cl.client.send("Clave recibida.")
                    print("La loopclave es: ", str(clave))

            #TODO: borrar esto
            print("La clave es: ", str(clave))

            if clave:
                hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
                firma = cifrar_hash(hash_md5, clave)
                resultado = f"{clave}\n{firma}\n{mensaje}\n0"
                guardar_resultado(resultado)
                print("Firma generada y guardada en salida.txt")
            else:
                print("No se pudo obtener la clave del servidor A")
        except:
            LOG.exception("Error al cifrar")

def opcion_firmar_mensaje() -> None:
    """
    Envia datos al proxy para firmar un mensaje.
    :return: None
    """
    print("=== Firmar Mensaje ===")
    identidad = input("\n Ingrese su identidad: \n")
    mensaje = input("Ingrese el mensaje a firmar: \n ")
    LOG.info(f"Cliente {cl.ADDR} solicitado firmar un mensaje.")
    resultado = f"{identidad}\n{mensaje}\n0"
    crear_archivo_entrada(resultado)
    procesar_archivo_entrada(identidad)



def opcion_autenticar_identidad() -> None:
    """
    Envia datos al proxy para autenticar identidad.
    :return: None
    """
    print("=== Autenticar Identidad ===")
    identidad = input("\nIngrese la clave de su usuario:\n ")
    LOG.info(f"Cliente {cl.ADDR} solicitado autenticar Identidad.")
    msg = "[AUTENTICAR] " + str(identidad) + " |!| "
    print(msg)
    cl.send(str(msg))

def eliminar_relleno(datos):
    longitud_relleno = datos[-1]
    return datos[:-longitud_relleno]

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
            print("hash_MD5 entrada", hash_entrada)
            print("hash_MD5 salida", hash_MD5_original)
            hash_md5_calculado = hashlib.md5(mensaje.encode()).hexdigest()
            print("Bloque Hash calculado:", hash_md5_calculado)

            if hash_MD5_original == hash_md5_calculado and hash_entrada == hash_md5_calculado:
                print("El mensaje es íntegro. Bloques Hash coinciden.")
            else:
                print("El mensaje no es íntegro. Bloques Hash no coinciden.")
        except:
            print("Error al descifrar el mensaje")


if __name__ == "__main__":
    # Crear logs para excepciones e informacion de estados.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler("client.log")],
    )

    ip = "localhost"
    LOG.info("[INICIANDO Cliente] el cliente está iniciando....")
    cl = Client(ip)
    detente: bool = False

    """Menu principal"""
    menu_opciones = {
        1: "1. Registrarse.",
        2: "2. Firmar mensaje.",
        3: "3. Autenticar Identidad.",
        4: "4. Descifrar Mensaje.",
        5: "5. Salir",
    }

    while not detente:
        print("=== Menú Principal ===")
        for key in menu_opciones.keys():
            print(key, "--", menu_opciones[key])
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            opcion_registrar_usuario()
        elif opcion == "2":
            opcion_firmar_mensaje()
        elif opcion == "3":
            opcion_autenticar_identidad()
        elif opcion == "4":
            descifrar_mensaje()
        elif opcion == "5":
            detente = True
            cl.send(cl.DISCONNECT_MESSAGE)
        else:
            print("\n Opción no válida. \n")
