# WebSocket Fibonacci

## Descrição

O **WebSocket Fibonacci** é uma API desenvolvida em **Python** com **FastAPI** que permite conexões WebSocket para cálculos da sequência de Fibonacci sob demanda.
A aplicação também gerencia os usuários conectados, armazenando as conexões em um banco de dados **Redis**.

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **WebSockets**
- **Redis**
- **Docker & Docker Compose**

---

## Como Rodar a Aplicação

A aplicação usa **perfis do Docker Compose**, permitindo rodar apenas o banco de dados (**db**) ou a aplicação completa (**full**).

### 🛠️ Rodando com Docker (Recomendado)

1. **Clone o repositório**

   ```sh
   git clone https://github.com/seu-usuario/websocket-fibonacci.git
   cd websocket-fibonacci
   ```

2. **Rodar apenas o banco de dados (Redis)**

   ```sh
   docker-compose --profile db up -d
   ```

3. **Rodar a aplicação completa (API + Redis)**

   ```sh
   docker-compose --profile full up --build
   ```

4. **A API estará rodando em:**
   ```
   ws://localhost:8000/ws
   ```

---

### 🛠️ Rodando Manualmente (Sem Docker)

1. **Instale as dependências**

   ```sh
   pip install -r requirements.txt
   ```

2. **Suba um servidor Redis** (se não estiver usando Docker)

   ```sh
   docker run -d --name redis -p 6379:6379 redis
   ```

3. **Inicie o servidor**

   ```sh
   python main.py
   ```

4. **A API estará disponível em:**
   ```
   ws://localhost:8000/ws
   ```

---

## Como Usar o Cliente WebSocket (`client.py`)

O repositório contém um **cliente WebSocket** (`client.py`) para testar a API.

### 🛠️ Rodando o cliente

1. **Com a API rodando**, execute o cliente:

   ```sh
   python client.py
   ```

2. **Funcionalidades do cliente**:
   - Exibe a **hora atual** recebida da API em tempo real.
   - Permite **enviar um número** para calcular **Fibonacci(n)**.
   - Exibe **o resultado** do cálculo Fibonacci quando recebido do servidor.

---

## Estrutura do Projeto

```
websocket-fibonacci/
│── client.py          # Cliente WebSocket para testar a API
│── Dockerfile         # Configuração do container da API
│── docker-compose.yml # Configuração do Docker
│── requirements.txt   # Dependências do projeto
├── src/
│   ├── main.py        # Servidor FastAPI WebSocket
│   ├── server.py      # Gerenciamento do WebSocket
│   ├── settings.py    # Configurações da aplicação
│   ├── fibonacci.py   # Cálculo de Fibonacci
└── ...
```

---
