import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:8765"  
    async with websockets.connect(uri) as websocket:
        print("Conectado ao servidor WebSocket!")
        await websocket.send("Olá, servidor!")
        response = await websocket.recv()
        print(f"Recebido do servidor: {response}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect_to_server())
