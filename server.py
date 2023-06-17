import asyncio
import sys
import socket
import logging

LOG = logging.getLogger("server")





async def main()->None:
    loop = asyncio.get_event_loop()
    server = await loop.create_server(start, host=host, port=port)
    LOG.info("Serving on {}:{}".format(host, port))

    try:
        await server.serve_forever()
    except KeyboardInterrupt as e:
        LOG.info("Keyboard interrupted. Exit.")

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
    asyncio.run(main())


