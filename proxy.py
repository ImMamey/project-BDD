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

    def eliminar_relleno(self, datos):
        longitud_relleno = datos[-1]
        return datos[:-longitud_relleno]

    def obtener_hash_entrada(self):
        with open("entrada.txt", "r") as archivo_entrada:
            identidad = archivo_entrada.readline().strip()
            mensaje = archivo_entrada.readline().strip()
            firma = archivo_entrada.readline().strip()
            hash_md5 = hashlib.md5(mensaje.encode()).hexdigest()
            return hash_md5

    # TODO: Cambiar printdebugs por LOGs en descifrar_mensaje
    # TODO: Esto debe de retornar un string al cliente.
    def descifrar_mensaje(self):
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
                MD5_descifrado = self.eliminar_relleno(MD5_descifrado)
                hash_MD5_original = MD5_descifrado.decode()
                print("este es la clave:", clave)
                print("este es el mensaje recibido:", mensaje)
                hash_entrada = self.obtener_hash_entrada()
                print("hash_MD5 entrada", hash_entrada)
                print("hash_MD5 salida", hash_MD5_original)
                hash_md5_calculado = hashlib.md5(mensaje.encode()).hexdigest()
                print("Bloque Hash calculado:", hash_md5_calculado)

                if hash_MD5_original == hash_md5_calculado and hash_entrada == hash_md5_calculado:
                    print("El mensaje es íntegro. Bloques Hash coinciden.")
                else:
                    print("El mensaje no es íntegro. Bloques Hash no coinciden.")
            except:
                LOG.exception("Error al descifrar el mensaje")

    #TODO: estos dos son los mismos, verificar que no se puedan combinar para reducir codigo.
    def guardar_resultado(self,resultado):
        with open("salida.txt", "w") as archivo_salida:
            archivo_salida.write(resultado)

    def crear_archivo_entrada(self, resultado):
        with open("entrada.txt", "w") as archivo_salida:
            archivo_salida.write(resultado)

    #TODO: Cambiar printdebugs por LOGs en processar_archivo_entrada
    #TODO: esto debe de retornar un string al cliente
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
                LOG.exception("Error al cifrar.")

    # TODO: Cambiar printdebugs por LOGs en processar_archivo_entrada
    # TODO: Esto debe de retornar un string al cliente.
    def autenticar_identidad(self,servidor_b,clave):
        servidor_b.send(("AUTENTICAR_IDENTIDAD " + clave).encode())
        respuesta = servidor_b.recv(1024).decode()
        if respuesta.startswith("USUARIO_EXISTE"):
            nombre = respuesta.split()[1]
            print("EL firmante existe.")
            print("Nombre: ", nombre)
            print("Clave: ", clave)
        else:
            print("El usuario no existe.")

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
            try:
                cedula: str = str(re_gex_despuesDelHeader.search(data).group())
                nombre: str = str(re_gex_despuesDelSeparador.search(data).group())
                LOG.info(
                    "Iniciado proceso para la opcion: %s con datos:\n cedula: %s\n Nombre: %s"
                    % (comando, cedula, nombre)
                )
                servidor_a.send(
                    ("REGISTRAR_USUARIO {} {}".format(int(cedula), nombre)).encode()
                )
                respuesta = servidor_a.recv(1024).decode().strip()
                print(respuesta)
            except:
                LOG.exception(
                    "No se pudo enviar o recibir respuesta para Registrar un usuario."
                )

        # TODO: Eliminar esta funcion
        elif comando == "FIRMAR":
            """e.g.: [FIRMAR] 24464628 |!| Habia una vez un perro feo"""
            try:
                identidad: str = str(re_gex_despuesDelHeader.search(data).group())
                mensaje: str = str(re_gex_despuesDelSeparador.search(data).group())
                LOG.info(
                    "Iniciado proceso para la opcion: %s con datos: \nIdentidad: %s \n Mensaje: %s"
                    % (comando, identidad, mensaje)
                )
                resultado = f"{identidad}\n{mensaje}\n0"
                self.crear_archivo_entrada(resultado)
                self.procesar_archivo_entrada(servidor_a, identidad)
            except:
                LOG.exception(
                    "No se pudo enviar o recibir respuesta para Firmar el mensaje."
                )
        # TODO: La respuesta debe de ser enviada al client.py, actualmente se envia es la consola de proxy.
        elif comando == "AUTENTICAR":
            """e.g.: [AUTENTICAR] 4568843548"""
            try:
                identidad: str = str(re_gex_despuesDelHeader.search(data).group())
                LOG.info(
                    "Iniciado proceso para la opcion: %s con el dato:\nIdentidad: %s"
                    % (comando, identidad)
                )
                self.autenticar_identidad(servidor_b,identidad)
            except:
                LOG.exception(
                "No se pudo autenticar la identidad."
                )

        # TODO: Eliminar esta función.
        elif comando == "VERIFICAR":
            """e.g.: [VERIFICAR] OWOWOWOWOWOWOOWOW |!| miguel"""
            #mensaje: str = str(re_gex_despuesDelHeader.search(data).group())
            #firma: str = str(re_gex_despuesDelSeparador.search(data).group())

            # TODO: implementar el código de hernani para verificar.
            # resultado = verificar_integridad(firma, mensaje)
            # guardar_resultado(resultado)
            LOG.info(
                "Iniciado proceso para la opcion: %s"
                % (comando)
            )
            try:
                self.descifrar_mensaje()
            except:
                LOG.exception(
                "No se pudo completar la petición de desciración/verificacion de integridad."
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
