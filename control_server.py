import asyncio
from typing import Tuple

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        if not message:
            break

        if message == "/shutdown":
            print("Сервер остановлен...")
            writer.write("Сервер остановлен...".encode())
            await writer.drain()
            server = writer.get_extra_info("server")
            server.close()
            await server.wait_closed()
            break
        else:
            response = f"Получено: {message}"
            writer.write(response.encode())
            await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main(host: str, port: int) -> None:
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Сервер запущен на {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    host = 'localhost'
    port = 9095
    asyncio.run(main(host, port))
