import asyncio


CONNECTION = set()


async def handle_echo(reader, writer):
    CONNECTION.add(writer)
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        if not data:
            writer.close()
            await writer.wait_closed()

        for text in CONNECTION:
            if text == writer:
                continue
            text.write(data)

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        await writer.drain()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
