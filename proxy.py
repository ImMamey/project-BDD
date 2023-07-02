import socket
import threading
import logging
import base64
import hashlib
from Crypto.Cipher import AES

LOG = logging.getLogger("Proxy Server")

clients = dict()


class Server:
    """
    Contiene todos los metodos necesarios para inciar un servidor usando Hilos.
    """

    class Network:
        """
        Contiene los atributos del servidor para facil acceso en una subclase anidada. Tambien crea el socket principal
        """

        def __init__(self) -> None:
            """
            :var SERVER: Guarda la IP del servidor
            :var PORT: Numero de puerto a usar
            :var ADDR: Tupla con los datos de: ip y numero de puerto
            :var FORMAT: Formato de encode
            :var DISCONNECT_MESSAGE: mensaje para la desconección y cierre de sesion.
            :var HEADER: Numero de bytes usado para algoritmo logico = como no sabemos cual es el tamaño de cada mensaje, todos los mensajes seran de 64 bytes. Facilita el encode/decode.
            :var server: socket del servidor.
            """
            # obtener lan ip
            ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ips.connect(("8.8.8.8", 80))

            """Usar este codigo para IP's LAN"""
            # self.SERVER: str = ips.getsockname()[0]
            self.SERVER: str = "localhost"
            # cerrar  lan ips
            ips.close()

            self.PORT: int = 5555  # purto a usar
            self.ADDR: tuple = (self.SERVER, self.PORT)
            self.FORMAT: str = "utf-8"
            self.DISCONNECT_MESSAGE: str = "!DISCONNECT"
            self.HEADER: int = 64

            self.server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.ADDR)

    def solicitar_clave(self, servidor_a, identidad):
        servidor_a.send(("SOLICITAR_CLAVE " + identidad).encode())
        clave = servidor_a.recv(1024).decode()
        return clave

    def cifrar_hash(self,hash_md5, clave):
        clave = clave.ljust(32)[:32]
        cifrador = AES.new(clave.encode(), AES.MODE_ECB)
        hash_bytes = hash_md5.encode()
        longitud_relleno = 16 - (len(hash_bytes) % 16)
        hash_relleno = hash_bytes + bytes([longitud_relleno] * longitud_relleno)
        hash_cifrado = cifrador.encrypt(hash_relleno)
        hash_cifrado_base64 = base64.b64encode(hash_cifrado).decode()
        return hash_cifrado_base64

    #TODO: estos dos son los mismos, verificar que no se puedan combinar para reducir codigo.
    def guardar_resultado(self,resultado):
        with open("salida.txt", "w") as archivo_salida:
            archivo_salida.write(resultado)

    def crear_archivo_entrada(self, resultado):
        with open("entrada.txt", "w") as archivo_salida:
            archivo_salida.write(resultado)

    def procesar_archivo_entrada(self,servidor_a, identidad2):
        with open("entrada.txt", "r") as archivo_entrada:
            identidad = archivo_entrada.readline().strip()
            mensaje = archivo_entrada.readline().strip()
            firma = archivo_entrada.readline().strip()
            try:
                clave = self.solicitar_clave(servidor_a, identidad2)
                if clave:
                    hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
                    firma = self.cifrar_hash(hash_md5, clave)
                    resultado = f"{clave}\n{firma}\n{mensaje}\n0"
                    self.guardar_resultado(resultado)
                    print("Firma generada y guardada en salida.txt")
                else:
                    print("No se pudo obtener la clave del servidor A")
            except:
                print("error al cifrar")

    def string_sampler(self, data: str, addr):
        """
        Esta funcion, permite verificar los datos enviados por cada cliente, y responde y filtra cada solicitud.
        :param data: Inofrmacion de cada cliente
        :return: la respuesta para el cliente.
        """
        import re

        re_gex_commando = re.compile(
            r"(?<=\[)(.*?)(?=\])"
        )  # regex para obtener el commando u opcion a enviar.
        re_gex_despuesDelHeader = re.compile(
            r"(?<=\])(.*?)(?=\|)"
        )  # codigo para obtener el campo despues del header: [...]
        re_gex_despuesDelSeparador = re.compile(
            r"(?<=\|!\|\s)(.*)"
        )  # codigo para obtener el campo despues del separador: |!|

        comando = str(re_gex_commando.search(data).group())

        #TODO: La respuesta debe de ser enviada al client.py, actualmente se envia es la consola de proxy.
        if comando == "REGISTRAR":
            """e.g.: [REGISTRAR] 24464628 |!| Victor"""
            cedula: str = str(re_gex_despuesDelHeader.search(data).group())
            nombre: str = str(re_gex_despuesDelSeparador.search(data).group())

            LOG.info(
                "Iniciado proceso para la opcion: %s con datos:\n cedula: %s\n Nombre: %s"
                % (comando, cedula, nombre)
            )
            try:
                servidor_a.send(
                    ("REGISTRAR_USUARIO {} {}".format(int(cedula), nombre)).encode()
                )
                respuesta = servidor_a.recv(1024).decode().strip()
                print(respuesta)
            except:
                LOG.exception(
                    "No se pudo enviar o recibir respuesta para Registrar un usuario."
                )

        elif comando == "FIRMAR":
            """e.g.: [FIRMAR] 24464628 |!| Habia una vez un perro feo"""
            identidad: str = str(re_gex_despuesDelHeader.search(data).group())
            mensaje: str = str(re_gex_despuesDelSeparador.search(data).group())

            # TODO: La respuesta debe de ser enviada al client.py, actualmente se envia es la consola de proxy.
            LOG.info(
                "Iniciado proceso para la opcion: %s con datos: \nIdentidad: %s \n Mensaje: %s"
                % (comando, identidad, mensaje)
            )
            try:
                resultado = f"{identidad}\n{mensaje}\n0"
                self.crear_archivo_entrada(resultado)
                self.procesar_archivo_entrada(servidor_a, identidad)
            except:
                LOG.exception(
                    "No se pudo enviar o recibir respuesta para Firmar el mensaje."
                )

        elif comando == "AUTENTICAR":
            """e.g.: [AUTENTICAR] 24464628"""
            identidad: str = str(re_gex_despuesDelHeader.search(data).group())

            # TODO: implementar el código de hernani para autenticar.
            # respuesta = autenticar_identidad(servidor_b, identidad)
            # guardar_resultado(respuesta)
            LOG.info(
                "Iniciado proceso para la opcion: %s con el dato:\nIdentidad: %s"
                % (comando, identidad)
            )

        elif comando == "VERIFICAR":
            """e.g.: [VERIFICAR] OWOWOWOWOWOWOOWOW |!| miguel"""
            mensaje: str = str(re_gex_despuesDelHeader.search(data).group())
            firma: str = str(re_gex_despuesDelSeparador.search(data).group())

            # TODO: implementar el código de hernani para verificar.
            # resultado = verificar_integridad(firma, mensaje)
            # guardar_resultado(resultado)
            LOG.info(
                "Iniciado proceso para la opcion: %s con datos: \n Mensaje: %s \nFirma: %s"
                % (comando, mensaje, firma)
            )

        # return respuesta

    def handle_client(self, conn, addr, n):
        """
        Metodo que maneja clientes, recibe mensajes y envia mensajes de confirmacion
        :param conn: connecion del socket.
        :param addr: tupla (ip,socket)
        :param n: Instancia de clase anidada "network"
        :return: None
        """
        LOG.info(f"[NUEVA CONNECCION] {addr} connectado.")

        connected: bool = True
        while connected:
            msg_length = conn.recv(n.HEADER).decode(n.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(n.FORMAT)
                self.string_sampler(msg, addr)
                if msg == n.DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg}")
                conn.send("[SERVIDOR] Mensaje recibido.".encode(n.FORMAT))

    def start(self):
        """
        Incia el servidor mediante un try and catch.
        :return:  None
        """
        try:
            n = self.Network()
            n.server.listen()
            LOG.info("El servidor esta activo en la IP: %s", n.SERVER)
            LOG.info("[Escuchando] Servidor esta escuchando...")
            while True:
                conn, addr = n.server.accept()
                thread = threading.Thread(
                    target=self.handle_client, args=(conn, addr, n)
                )
                thread.start()
                LOG.info(f"[CONNECIONES ACTIVAS] {threading.active_count() - 1}")

        except Exception as e:
            LOG.exception("Error al inicar el servidor.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler("proxy.log")],
    )

    try:
        host = "localhost"
        puerto_a = 5000
        puerto_b = 5001
        servidor_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_a.connect((host, puerto_a))
        servidor_b.connect((host, puerto_b))
    except Exception as e:
        LOG.exception("Error al conectarse con los servidores A y B.")

    LOG.info("[INICIANDO SERVIDOR] el servidor está iniciando....")
    s = Server()
    s.start()
