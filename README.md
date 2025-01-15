# Serviço Simples de Autenticação de Utilizadores

Esta aplicação é uma API desenvolvida em Flask que permite o registo, login e logout de utilizadores, com suporte para autenticação segura usando JWT e hashing de passwords com bcrypt.

---

## Passos para Executar a Aplicação

1. **Crie um Ambiente Virtual**

   - No diretório do projeto, crie um ambiente virtual:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **Linux/Mac**:
       ```bash
       source venv/bin/activate
       ```

2. **Crie o arquivo `.env`**

   - Na raiz do projeto, crie um arquivo chamado `.env`.
   - Adicione as seguintes variáveis:
     ```env
     SECRET_KEY=sua_chave_secreta_aqui
     JWT_SECRET_KEY=sua_chave_secreta_para_jwt
     JWT_HEADER_NAME=x-token
     ```

3. **Instale os Pacotes Necessários**

   - Certifique-se de estar com o ambiente virtual ativado.
   - Instale os pacotes listados no arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Execute a Aplicação**

   - No terminal, com o ambiente virtual ativado, execute o arquivo principal:
     ```bash
     python main.py
     ```
   - A aplicação será iniciada no endereço padrão: `http://127.0.0.1:5000`.

---

## Endpoints Disponíveis

### 1. **Registo de Utilizador**

- **URL**: `/auth/create_user`
- **Método**: `POST`
- **Descrição**: Regista um novo utilizador com um nome de utilizador único e uma password segura.
- **Cabeçalho**:

  ```json
  Content-Type: application/json
  ```

- **Body (JSON)**:

```json
{
  "username": "john_doe",
  "password": "SecurePassword@123"
}
```

### Requisitos da Password:

- Deve incluir pelo menos:
  - Uma letra maiúscula.
  - Uma letra minúscula.
  - Um número.
  - Um caracter especial (`!@#$%^&*`).
- Comprimento entre **8 e 32 caracteres**.

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "User registered successfully!",
  "data": {
    "id": 1000,
    "username": "jhon_doe",
    "date_created": "2025-01-15 12:25:00"
  }
}
```

- **Resposta de Erro (409 - Username em Uso)**:

```json
{
  "success": false,
  "message": "Validations errors",
  "errors": {
    "username": ["Username already being used!"]
  }
}
```

- **Resposta de Erro (400 - Erros de Validação)**:

```json
{
  "success": false,
  "message": "Validation errors occurred.",
  "errors": {
    "password": [
      "Password must include at least one uppercase letter, one lowercase letter, one number, and one special character, and be between 8 and 32 characters long"
    ]
  }
}
```

```json
{
  "success": false,
  "message": "Validations errors",
  "errors": {
    "username": ["username is a required field!"],
    "password": ["password is a required field!"]
  }
}
```

### 2. **Login**

- **URL**: `/auth/user_login`
- **Método**: `POST`
- **Descrição**: Autentica o utilizador e retorna um token JWT.
- **Cabeçalho**:

  ```json
  Content-Type: application/json
  ```

  - **Body (JSON)**:

  ```json
  {
    "username": "john_doe",
    "password": "SecurePassword@123"
  }
  ```

  - **Resposta de Sucesso (200)**:

  ```json
  {
    "success": true,
    "message": "Login successful!",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

  - **Resposta de Erro (401 - Credenciais Inválidas)**:

  ```json
  {
    "success": false,
    "message": "Invalid username or password!"
  }
  ```

### 3. **Logout**

- **URL**: `/auth/user_logout`
- **Método**: `POST`
- **Descrição**: Revoga o token JWT atual, invalidando a sessão.
- **Cabeçalho**:

  ```json
  x-token: <JWT_TOKEN>
  ```

- **Body (JSON)**:

```json
{
  "username": "john_doe"
}
```

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "User logged out successfully!"
}
```

- **Resposta de Erro (401 - Token Expirado)**:

```json
{
  "msg": "Token has been revoked"
}
```

## Estrutura do Projeto

. ├── app/
│ ├── init.py
│ ├── configs.py
│ ├── routes.py
│ └── validators.py
├── venv/
├── .env
├── main.py
├── requirements.txt
└── README.md

## Observações

Certifique-se de que o arquivo `.env` contém as variáveis:

- **`SECRET_KEY`**: Chave usada para segurança geral do Flask.
- **`JWT_SECRET_KEY`**: Chave secreta usada para gerar e validar tokens JWT.
- **`JWT_HEADER_NAME`**: Nome do cabeçalho personalizado usado para o token (padrão: `x-token`).

  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - **Linux/Mac**:
    ```bash
    source venv/bin/activate
    ```

---

## Demonstração

- **Local**: `http://127.0.0.1:5000/`
- **Hospedado**: 