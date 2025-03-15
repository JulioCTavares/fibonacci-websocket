from typing import List
from fastapi import WebSocket
from fibonacci import calculate_fibonacci  

class WebSocketServer:
    def __init__(self):
        self.clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.clients.remove(websocket)
        await websocket.close()

    async def send_fibonacci(self, n: int):
        fibonacci_result = calculate_fibonacci(n)
        
        return fibonacci_result
