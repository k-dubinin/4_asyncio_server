import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")

    writer.write(data)
    await writer.drain()
    writer.close()

async def main(host, port):
    server = await asyncio.start_server(handle_echo, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    host = 'localhost'
    port = 9090
    asyncio.run(main(host, port))
