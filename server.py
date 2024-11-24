import asyncio
import websockets
import os

# 存储所有连接的 WebSocket 客户端
connected_clients = set()

# 用于保存文本消息的文件
text_file_path = "received_texts.txt"

async def echo(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            if isinstance(message, str):
                # 如果是字符串类型，说明是文本消息
                print("Received text from client:", message)  # 打印接收到的文本消息
                # 将文本消息存储在文件中
                with open(text_file_path, "a") as f:  # 以追加模式打开文件
                    f.write(message + "\n")  # 每条消息换行存储
                # 不转发文本消息到客户端
            else:
                # 处理图像数据（即二进制消息）
                print("Received image frame from client")  # 打印接收到的图像数据
                # 将接收到的视频帧转发给所有连接的客户端
                for client in connected_clients:
                    await client.send(message)

    finally:
        connected_clients.remove(websocket)

# WebSocket 服务器
async def server():
    async with websockets.serve(echo, "2409:891b:f050:479:34d6:8722:7c3a:b794", 8081):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(server())
