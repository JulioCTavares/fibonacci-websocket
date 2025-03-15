from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from server import WebSocketServer
from settings import WS_HOST, WS_PORT
import uvicorn
from fibonacci import calculate_fibonacci

app = FastAPI()
server = WebSocketServer()

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await server.connect(websocket)
    try:
        while True:
            await websocket.send_text("Menu de opções:\n1. Calcular Fibonacci\n2. Sair")

            message = await websocket.receive_text()

            if message == "1":
                await websocket.send_text("Digite um número para calcular o Fibonacci:")
                n = int(await websocket.receive_text())
                fibonacci_result = calculate_fibonacci(n)
                await websocket.send_text(f"Resultado do Fibonacci para {n}: {fibonacci_result}")
            elif message == "2":
                await websocket.send_text("Desconectando...")
                await server.disconnect(websocket)
                break
            else:
                await websocket.send_text("Opção inválida, tente novamente.")
    except WebSocketDisconnect:
        await server.disconnect(websocket)

def start_server():
    uvicorn.run(app, host=WS_HOST, port=WS_PORT)

def main():
    print("Servidor WebSocket iniciado...")
    start_server()

if __name__ == "__main__":
    main()
