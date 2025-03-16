import asyncio
from fastapi import WebSocket
from typing import Dict
from fibonacci import calculate_fibonacci
from datetime import datetime
import redis.asyncio as redis
from settings import REDIS_URL
from starlette.websockets import WebSocketState
import json


class WebSocketServer:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        self.redis = None
        self._time_update_task = None
        self.last_sent_time = ""

    async def init_redis(self):
        if self.redis is None:
            try:
                self.redis = await redis.from_url(REDIS_URL, decode_responses=True)
                await self.redis.delete("connected_users")
                print("Conexão com Redis estabelecida com sucesso.")
            except Exception as e:
                print(f"Erro ao conectar ao Redis: {e}")
                self.redis = None

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        client_id = user_id or str(id(websocket))
        self.clients[client_id] = websocket

        await self.init_redis()

        if self.redis:
            user_data = {
                "id": client_id,
                "connected_at": datetime.now().isoformat(),
                "ip": str(websocket.client.host)
            }
            await self.redis.hset("connected_users", client_id, json.dumps(user_data))

        if self._time_update_task is None or self._time_update_task.done():
            self._time_update_task = asyncio.create_task(self.send_time_updates())

        if self.redis:
            await self.redis.set("user_count", len(self.clients))

        print(f"Cliente {client_id} conectado. Total de clientes: {len(self.clients)}")
        return client_id

    async def disconnect(self, client_id: str):
        if client_id in self.clients:
            websocket = self.clients[client_id]
            try:
                await websocket.close()
            except:
                pass  
            del self.clients[client_id]

            if self.redis:
                await self.redis.hdel("connected_users", client_id)
                await self.redis.set("user_count", len(self.clients))

            print(f"Cliente {client_id} desconectado. Total de clientes: {len(self.clients)}")

        if not self.clients and self._time_update_task:
            self._time_update_task.cancel()
            self._time_update_task = None

    async def send_fibonacci(self, client_id: str, n: int):
        if client_id in self.clients:
            websocket = self.clients[client_id]
            try:
                print(f"Calculando Fibonacci({n}) para cliente {client_id}")
                fibonacci_result = calculate_fibonacci(n)
                response = {
                    "type": "fibonacci_result",
                    "n": n,
                    "result": fibonacci_result
                }
                await websocket.send_json(response)
                print(f"Resultado enviado: Fibonacci({n}) = {fibonacci_result}")
            except Exception as e:
                print(f"Erro ao enviar resultado Fibonacci: {e}")
                await self.disconnect(client_id)

    async def send_time_updates(self):
        try:
            print("Iniciando tarefa de envio de atualizações de tempo")
            while self.clients:  # Continua enquanto houver clientes
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if now != self.last_sent_time:
                    self.last_sent_time = now

                    time_message = {
                        "type": "time_update",
                        "timestamp": now
                    }

                    to_disconnect = []

                    for client_id, websocket in list(self.clients.items()):
                        try:
                            if websocket.client_state == WebSocketState.CONNECTED:
                                await websocket.send_json(time_message)
                            else:
                                to_disconnect.append(client_id)
                        except Exception:
                            to_disconnect.append(client_id)

                    for client_id in to_disconnect:
                        await self.disconnect(client_id)

                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Tarefa de envio de tempo cancelada")
        except Exception as e:
            print(f"Erro na tarefa de envio de tempo: {e}")

    async def handle_message(self, client_id: str, message: str):
        if client_id not in self.clients:
            return

        try:
            print(f"Mensagem recebida do cliente {client_id}: {message}")

            try:
                data = json.loads(message)
                msg_type = data.get("type", "")

                if msg_type == "fibonacci":
                    n = int(data.get("n", 0))
                    if n >= 0:
                        await self.send_fibonacci(client_id, n)
                    else:
                        await self.clients[client_id].send_json({
                            "type": "error",
                            "message": "Número deve ser não-negativo"
                        })

            except json.JSONDecodeError:
                if message.strip().isdigit():
                    n = int(message)
                    await self.send_fibonacci(client_id, n)
                else:
                    await self.clients[client_id].send_json({
                        "type": "error",
                        "message": "Comando não reconhecido"
                    })

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            await self.disconnect(client_id)

    async def get_connected_users(self):
        if not self.redis:
            return []

        users = await self.redis.hgetall("connected_users")
        return [json.loads(user_data) for user_data in users.values()]