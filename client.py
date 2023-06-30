import socket
import re
import sys
import logging

LOG = logging.getLogger("Cliente")
class Client:
    """
    Contiene todos los metodos para el cliente.
    """
    def __init__(self,ip) -> None:
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
        self.FORMAT: str = 'utf-8'
        self.DISCONNECT_MESSAGE: str = "!DISCONNECT"
        self.SERVER: str = ip
        self.ADDR: tuple = (self.SERVER, self.PORT)
        LOG.info(f"[NUEVO CLIENTE] {self.ADDR} conectado.")

        self.start()

    def start(self)->None:
        """
        Inicia el socket del cliente, se conectara a la tupla con los datos del servidor
        :return: None
        """
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
        except Exception as e:
            LOG.exception(
                "Error al tratarse de conectar al Proxy. " +
                "Por favor cerrar el cliente y verificar la coneccion."
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
            send_length = str(msg_length).encode(self.FORMAT) #chequea que los mensajes sean de 64bytes
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length) #se envia los mensajes
            self.client.send(message)
            print(self.client.recv(2048).decode(self.FORMAT))
        except Exception as e:
            LOG.exception("Error al enviar el mensaje.")



def opcion_registrar_usuario(servidor_a)->None:
    print("=== Registro de Usuario ===")
    cedula = input("\nIngrese su cédula:\n ")
    nombre = input("Ingrese su nombre:\n ")

    #servidor_a.send(("REGISTRAR_USUARIO {} {}".format(cedula, nombre)).encode())
    #respuesta = servidor_a.recv(1024).decode().strip()

    #print(respuesta)

    #logging/debuggin
    LOG.info(f"Cliente {cl.ADDR} solicitado Registrar un cliente.")
    msg = "[REGISTRAR] " + str(cedula) + " |!| " + str(nombre)
    print(msg)

    cl.send(str(msg))

def opcion_firmar_mensaje()->None:
    print("=== Firmar Mensaje ===")
    identidad = input("\n Ingrese su identidad: \n")
    mensaje = input("Ingrese el mensaje a firmar: \n ")
    #resultado = opcion_firmar_mensaje(servidor_a, identidad, mensaje)
    #guardar_resultado(resultado)

    #Logging/debbuggin
    LOG.info(f"Cliente {cl.ADDR} solicitado firmar un mensaje.")
    msg = "[FIRMAR] " + str(identidad) + " |!| " + str(mensaje)
    print(msg)

    cl.send(str(msg))

def opcion_autenticar_identidad()->None:
    print("=== Autenticar Identidad ===")
    identidad = input("\nIngrese su identidad:\n ")
    #respuesta = autenticar_identidad(servidor_b, identidad)
    #guardar_resultado(respuesta)

    # Logging/debbuggin
    LOG.info(f"Cliente {cl.ADDR} solicitado autenticar Identidad.")
    msg = "[AUTENTICAR] " + str(identidad)
    print(msg)

def opcion_verificar_integridad()->None:
    print("=== Verificar Integridad ===")
    mensaje = input("\nIngrese el mensaje: \n")
    firma = input("Ingrese la firma del mensaje: \n")
    #resultado = verificar_integridad(firma, mensaje)
    #guardar_resultado(resultado)

    # Logging/debbuggin
    LOG.info(f"Cliente {cl.ADDR} solicitado verificar integridad.")
    msg = "[VERIFICAR] " + str(mensaje) + " |!| " + str(firma)
    print(msg)

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler("client.log")],
    )

    ip = "localhost"
    LOG.info("[INICIANDO Cliente] el servidor está iniciando....")
    cl = Client(ip)
    detente: bool = False

    """Menu principal"""
    menu_opciones = {
        1: "1. Registrarse.",
        2: "2. Firmar mensaje.",
        3: "3. Autenticar Identidad.",
        4: "4. Verificar Integridad.",
        5: "5. Salir"
    }

    print("=== Menú Principal ===")
    for key in menu_opciones.keys():
        print(key, '--', menu_opciones[key])
    while not detente:
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            opcion_registrar_usuario()
        elif opcion == "2":
            opcion_firmar_mensaje()
        elif opcion == "3":
            opcion_autenticar_identidad()
        elif opcion == "4":
            opcion_verificar_integridad()
        elif opcion == "5":
            detente=True
            cl.send(cl.DISCONNECT_MESSAGE)
        else:
            print("Opción no válida.")

    #TODO: funcion depreciada, borrar una vez que pierda utilidad.
    while not detente:
        msg: str = input("Escriba un mensaje para enviar al Servidor (escriba \"n\" para detener)\n")
        if msg=="n":
            detente=True
            cl.send(cl.DISCONNECT_MESSAGE)
        else:
            cl.send(str(msg))