#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio


async def init_socket (loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 3000, loop=loop)
    return reader, writer


async def tcp_ping(writer, loop):
    while True:
        print('Send: ping')
        writer.write("ping".encode())
        print("ping sent")
        await asyncio.sleep(3)
        print("sleep finished")


async def tcp_read(reader, loop):
    while True:
        data = await reader.read(100)
        print('Received: %r' % data.decode())


def main():
    reader = None
    writer = None
    loop = asyncio.get_event_loop()
    reader, writer = loop.run_until_complete(init_socket(loop))
    tasks = [
        tcp_read(reader, loop),
        tcp_ping(writer, loop),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    writer.close()


if __name__ == "__main__":
    main()