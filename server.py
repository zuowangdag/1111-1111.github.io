import asyncio
import websockets

connected_clients = set()
text_file_path = "received_texts.txt"

async def echo(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            if isinstance(message, str):
                print("Received text from client:", message)
                with open(text_file_path, "a") as f:
                    f.write(message + "\n")
            else:
                print("Received image frame from client")
                for client in connected_clients:
                    await client.send(message)
    finally:
        connected_clients.remove(websocket)

async def server():
    async with websockets.serve(echo, "0.0.0.0", 8081):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(server())
