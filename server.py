import asyncio
import websockets

clients = set()  

async def handler(websocket):
    clients.add(websocket)
    print("Novo cliente conectado!")
    
    try:
        while True:
            message = await websocket.recv()
            print(f"Mensagem recebida: {message}")
            await websocket.send(f"Mensagem recebida: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Cliente desconectado.")
    finally:
        clients.remove(websocket)

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Servidor WebSocket iniciado em ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
