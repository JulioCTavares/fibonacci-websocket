import asyncio
import websockets
import json
import sys
from datetime import datetime

class WebSocketClient:
    def __init__(self, uri='ws://localhost:8000/'):
        self.uri = uri
        self.websocket = None
        self.client_id = None
        self.running = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.running = True

            welcome = await self.websocket.recv()
            welcome_data = json.loads(welcome)
            self.client_id = welcome_data.get('client_id')
            print(f"Conectado ao servidor! ID do cliente: {self.client_id}")

            await asyncio.gather(
                self.receive_messages(),
                self.send_commands()
            )
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.running = False

    async def receive_messages(self):
        try:
            while self.running and self.websocket:
                message = await self.websocket.recv()

                try:
                    data = json.loads(message)
                    message_type = data.get('type', '')

                    if message_type == 'time_update':
                        print(f"\rHora atual: {data['timestamp']}", end='', flush=True)
                    elif message_type == 'fibonacci_result':
                        print(f"\nFibonacci({data['n']}) = {data['result']}")
                    elif message_type == 'error':
                        print(f"\nErro: {data['message']}")
                    else:
                        print(f"\nMensagem recebida: {data}")

                except json.JSONDecodeError:
                    print(f"\nMensagem recebida: {message}")

        except websockets.exceptions.ConnectionClosed:
            print("\nConexão fechada pelo servidor")
            self.running = False
        except Exception as e:
            print(f"\nErro ao receber mensagens: {e}")
            self.running = False

    async def send_fibonacci_request(self, n):
        try:
            request = json.dumps({
                "type": "fibonacci",
                "n": n
            })
            await self.websocket.send(request)
        except Exception as e:
            print(f"Erro ao enviar solicitação: {e}")

    async def send_commands(self):
        try:
            print("\nDigite um número para calcular Fibonacci ou 'q' para sair")
            while self.running:
                await asyncio.sleep(0.1)
                if not sys.stdin.isatty():
                    continue

                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline().strip()

                    if line.lower() == 'q':
                        print("Desconectando...")
                        self.running = False
                        break

                    try:
                        n = int(line)
                        await self.send_fibonacci_request(n)

                    except ValueError:
                        print("Por favor, digite um número inteiro válido ou 'q' para sair")

                    print("\nDigite um número para calcular Fibonacci ou 'q' para sair")

        except Exception as e:
            print(f"Erro ao enviar comandos: {e}")
            self.running = False

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.running = False

async def main():
    client = WebSocketClient()
    try:
        await client.connect()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    import select
    print("Iniciando cliente WebSocket...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário")