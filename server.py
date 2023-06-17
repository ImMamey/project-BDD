import asyncio
import sys
import socket
import logging

LOG = logging.getLogger("server")

def start()->None:
    """Inicia el servidor"""
    print("OWO")



def main()->None:
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(start, host=host, port=port)
    print("before run coro")

    try:
        server = loop.run_until_complete(coro)
        LOG.info("Serving on {}:{}".format(host, port))
        print("Serving on {}:{}".format(host, port))
    except Exception as e:
        exception: str = f"{type(e).__name__}: (e)"
        LOG.exception(f"Fallo al correr la corutina: \n {exception} \n ")
        print(f"Fallo al correr la corutina: \n {exception} \n ")
        LOG.info("Keyboard interrupted. Exit.")
    loop.run_forever()
    #cerrar el servidor
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":

    try:
        ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ips.connect(("8.8.8.8", 80))
        host: str = ips.getsockname()[0]
        ips.close()
    except Exception as e:
        exception: str = f"{type(e).__name__}: (e)"
        LOG.exception(
            f"Fallo al cargar la IP public del servidor: \n {exception} \n "
            + f"Se montará el servidor en localhost: 127.0.0.1"
        )
        host: str = "127.0.0.1"

    port = 5555
    main()


