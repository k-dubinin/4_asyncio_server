import asyncio
from typing import AsyncIterator

async def scan_port(host: str, port: int) -> bool:
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
        return True
    except OSError:
        return False

async def scan_ports(host: str, ports: range) -> AsyncIterator[int]:
    sem = asyncio.Semaphore(1000)  # Ограничение одновременных соединений
    async with sem:
        tasks = [scan_port(host, port) for port in ports]
        results = await asyncio.gather(*tasks)
        for port, is_open in zip(ports, results):
            if is_open:
                yield port

async def main():
    host = input("Введите имя хоста или IP-адрес: ")
    ports = range(1, 1025)  # Сканирование общих портов
    async for port in scan_ports(host, ports):
        print(f"Порт {port} открыт")

if __name__ == "__main__":
    asyncio.run(main())
