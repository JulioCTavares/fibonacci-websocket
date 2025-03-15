from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from server import WebSocketServer
from settings import WS_HOST, WS_PORT
from contextlib import asynccontextmanager
import uvicorn
import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
    await server.init_redis()
    yield
    if server.redis:
        await server.redis.aclose()

app = FastAPI(lifespan=lifespan)
server = WebSocketServer()

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    client_id = str(uuid.uuid4())
    await server.connect(websocket, client_id)

    try:
        await websocket.send_json({
            "type": "welcome",
            "message": "Conectado ao servidor WebSocket",
            "client_id": client_id
        })

        while True:
            message = await websocket.receive_text()
            await server.handle_message(client_id, message)

    except WebSocketDisconnect:
        await server.disconnect(client_id)
    except Exception as e:
        print(f"Erro na conexão WebSocket: {e}")
        await server.disconnect(client_id)



def start_server():
    uvicorn.run(app, host=WS_HOST, port=WS_PORT)

if __name__ == "__main__":
    print(f"Servidor WebSocket iniciado em ws://{WS_HOST}:{WS_PORT}/ws")
    start_server()