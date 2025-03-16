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
   ws://localhost:8000/
   ```

---

### 🛠️ Rodando Apenas o Banco de Dados no Docker

1. **Crie um ambiente virtual**

   ```sh
   python3 -m venv .venv
   ```

2. **Ative o ambiente**

   - Linux/MacOS:

   ```sh
   source venv/bin/activate
   ```

   - Windows

   ```sh
   venv\Scripts\activate
   ```

3. **Instale as dependências**

   ```sh
   pip install -r requirements.txt
   ```

4. **Suba um servidor Redis**

   ```sh
   docker-compose --profile db up --build
   ```

5. **Inicie o servidor**

   ```sh
   python main.py
   ```

6. **O servidor estará disponível em:**
   ```
   ws://localhost:8000/
   ```

---

## Como Usar o Cliente WebSocket (`client.py`)

O repositório contém um **cliente WebSocket** (`client.py`) para testar a API.

### 🛠️ Rodando o cliente

1. **Crie um ambiente virtual (recomendado no modo full):**

   ```sh
   python3 -m venv .venv
   ```

2. **Ative o ambiente**

   - Linux/MacOS:

   ```sh
   source venv/bin/activate
   ```

   - Windows

   ```sh
   venv\Scripts\activate
   ```

3. **Instale as dependências**

   ```sh
   pip install -r requirements.txt
   ```

4. **Com a API rodando**, execute o cliente:

   ```sh
   python client.py
   ```

5. **Funcionalidades do cliente**:
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
