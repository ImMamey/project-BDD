import socket
import threading
import logging
# TODO: eliminar LAN, hacerlo local.

LOG = logging.getLogger("server")

clients = dict()

class Server:
    """
    Contiene todos los metodos necesarios para inciar un servidor usando Hilos.
    """
    class Network:
        """
        Contiene los atributos del servidor para facil acceso en una subclase anidada. Tambien crea el socket principal
        """
        def __init__(self)-> None:
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


            self.SERVER: str = ips.getsockname()[0]
            #cerrar  lan ips
            ips.close()

            self.PORT: int = 5555 #purto a usar
            self.ADDR: tuple = (self.SERVER, self.PORT)
            self.FORMAT: str = 'utf-8'
            self.DISCONNECT_MESSAGE: str= "!DISCONNECT"
            self.HEADER: int =64

            self.server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.ADDR)

    def handle_client(self, conn, addr,n):
        """
        Metodo que maneja clientes, recibe mensajes y envia mensajes de confirmacion
        :param conn: connecion del socket.
        :param addr: tupla (ip,socket)
        :param n: Instancia de clase anidada "network"
        :return: None
        """
        print(f"[NUEVA CONNECCION] {addr} connectado.")

        connected: bool = True
        while connected:
            msg_length= conn.recv(n.HEADER).decode(n.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(n.FORMAT)
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
            LOG.info("El servidor esta activo en la IP: %s",n.SERVER)
            LOG.info("[Escuchando] Servidor esta escuchando...")
            while True:
                conn, addr = n.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, n))
                thread.start()
                LOG.info(f"[CONNECIONES ACTIVAS] {threading.active_count() - 1}")

        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al Iniciar el servidor. El error fue: \n{exception}")



if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler("stuff.log")],
    )

    if __name__ == "__main__":
        LOG.info("[INICIANDO SERVIDOR] el servidor está iniciando....")
        s = Server()
        s.start()
