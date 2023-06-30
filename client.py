import socket
import re
import sys

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
        self.SERVER: str = ip #"192.168.56.1"
        self.ADDR: tuple = (self.SERVER, self.PORT)

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
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al tratar de conectarse al servidor: \n{exception}")
            sys.exit("El cliente se cerrará despues de el log....")


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
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al enviar el mensaje: \n{exception}")



def opcion_registrar_usuario(servidor_a)->None:
    print("=== Registro de Usuario ===")
    cedula = input("Ingrese su cédula: ")
    nombre = input("Ingrese su nombre: ")

    servidor_a.send(("REGISTRAR_USUARIO {} {}".format(cedula, nombre)).encode())
    respuesta = servidor_a.recv(1024).decode().strip()

    print(respuesta)
def opcion_firmar_mensaje()->None:
    identidad = input("Ingrese su identidad: ")
    mensaje = input("Ingrese el mensaje a firmar: ")
    resultado = opcion_firmar_mensaje(servidor_a, identidad, mensaje)
    guardar_resultado(resultado)

def opcion_autenticar_identidad()->None:
    identidad = input("Ingrese su identidad: ")
    respuesta = autenticar_identidad(servidor_b, identidad)
    guardar_resultado(respuesta)

def opcion_verificar_integridad()->None:
    mensaje = input("Ingrese el mensaje: ")
    firma = input("Ingrese la firma del mensaje: ")
    resultado = verificar_integridad(firma, mensaje)
    guardar_resultado(resultado)

if __name__ == "__main__":
    detente: bool = False
    """ Esto no es necesario anymore, ya que será local host.
    while not detente:
        ip: str= input("Escriba el ip del servidor:\n")
        pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not pattern.match(ip):
            print("La ip no es válida. Intente nuevamente: \n")
        else:
            detente = True
    """

    ip = "localhost"
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
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        opcion_registrar_usuario(servidor_a)
    elif opcion == "2":
        opcion_firmar_mensaje()
    elif opcion == "3":
        opcion_autenticar_identidad()
    elif opcion == "4":
        opcion_verificar_integridad()
    else:
        print("Opción no válida.")

    while not detente:
        msg: str = input("Escriba un mensaje para enviar al Servidor (escriba \"n\" para detener)\n")
        if msg=="n":
            detente=True
            cl.send(cl.DISCONNECT_MESSAGE)
        else:
            cl.send(str(msg))