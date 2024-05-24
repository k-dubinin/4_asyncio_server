import asyncio

class ChatServer:
    def __init__(self):
        self.users = {}
        self.history = []

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")

        while True:
            data = await reader.read(100)
            message = data.decode().strip()
            if not message:
                break

            if message.startswith("/login "):
                username = message.split()[1]
                self.users[username] = writer
                print(f"{username} joined the chat")
            elif message.startswith("/logout"):
                username = [key for key, value in self.users.items() if value == writer]
                if username:
                    del self.users[username[0]]
                    print(f"{username[0]} left the chat")
            else:
                self.history.append(message)
                for user, user_writer in self.users.items():  # Renamed the variable to avoid conflict with the parameter name
                    user_writer.write(data)
                    await user_writer.drain()

    async def run_server(self, host, port):
        server = await asyncio.start_server(self.handle_client, host, port)
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    host = 'localhost'
    port = 9095
    chat_server = ChatServer()
    asyncio.run(chat_server.run_server(host, port))
