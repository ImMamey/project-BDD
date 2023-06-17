import asyncio
import sys
import socket
import logging

LOG = logging.getLogger("server")

clients = dict()


def client_connected_cb(client_reader, client_writer) -> None:
    """Inicia el servidor"""
    client_id = client_writer.get_extra_info("peername")
    LOG.info("Client connected: {}".format(client_id))


async def main() -> None:
    server = await asyncio.start_server(client_connected_cb, host=host, port=port)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    LOG.info(f"Serving on:{addrs}")

    try:
        async with server:
            await server.serve_forever()
    except Exception as e:
        exception: str = f"{type(e).__name__}: (e)"
        LOG.exception("Fallo al correr la corutina del servidor")


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler("stuff.log")],
    )

    try:
        ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ips.connect(("8.8.8.8", 80))
        host: str = ips.getsockname()[0]
        ips.close()
    except Exception as e:
        exception: str = f"{type(e).__name__}: (e)"
        LOG.exception(
                "Fallo al cargar la IP publica del servidor\n"
                "Se montará el servidor en localhost: 127.0.0.1"
        )
        host: str = "127.0.0.1"

    port = 5555
    asyncio.run(main())
