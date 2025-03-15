import websockets
import asyncio

async def connect_to_server():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        print("Conectado ao servidor!")

        while True:
            menu = await websocket.recv()
            print(menu)
            option = input("Escolha uma opção: ")
            await websocket.send(option)

            if option == "1":
                try:
                    n = int(input("Digite um número para calcular o Fibonacci: "))
                    await websocket.send(str(n))
                    await websocket.recv()
                except ValueError:
                    print("Por favor, digite um número válido.")
            elif option == "2":
                print("Desconectando do servidor...")
                break

if __name__ == "__main__":
    asyncio.run(connect_to_server())
