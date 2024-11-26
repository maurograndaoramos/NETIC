# Documentação da Classe `mongo_remote_db`

A classe `mongo_remote_db` foi projetada para conectar a um banco de dados MongoDB remoto e oferece métodos para gerenciar documentos de chats e mensagens. Abaixo está a descrição dos métodos e seus propósitos.

---

## Construtor `__init__(self)`

### Descrição
Conecta-se ao banco de dados MongoDB e configura a coleção de chats.

### Atributos
- `uri`: String de conexão do MongoDB.
- `client`: Instância de `MongoClient` para conectar ao MongoDB.
- `db`: Banco de dados nomeado como `"chat_db"`.
- `chat_collection`: Coleção de chats chamada `"chats"`.

Caso a coleção de chats não exista, ela será criada.

---

## Método `get_all_chats(self)`

### Descrição
Retorna todos os documentos de chat presentes na coleção de chats.

### Retorno
Lista de todos os chats armazenados no banco de dados.

---

## Método `get_messages(self, chat_id)`

### Descrição
Obtém todas as mensagens de um chat específico, identificado pelo `chat_id`.

### Parâmetros
- `chat_id` : ID do chat no banco de dados MongoDB.

### Retorno
Lista de mensagens contidas no chat identificado.

---

## Método `get_chats(self, user_id)`

### Descrição
Retorna todos os chats em que um usuário específico (`user_id`) participa.

### Parâmetros
- `user_id` : ID do usuário para o qual serão buscados os chats.

### Retorno
Lista de chats que incluem o usuário especificado.

---

## Método `get_or_create_chat(self, user_id=None, friend_id=None, chat_id=None)`

### Descrição
Obtém um chat entre dois usuários específicos, ou cria um novo chat caso não exista.

### Parâmetros
- `user_id` : ID do usuário atual.
- `friend_id` : ID do amigo com quem o usuário está conversando.
- `chat_id` : ID opcional do chat a ser buscado diretamente.

### Retorno
Documento do chat entre `user_id` e `friend_id` (existente ou recém-criado).

---

## Método `add_message(self, chat_id, user_id, msg_content)`

### Descrição
Adiciona uma nova mensagem a um chat específico.

### Parâmetros
- `chat_id` : ID do chat onde a mensagem será adicionada.
- `user_id` : ID do usuário que está enviando a mensagem.
- `msg_content` : Conteúdo da mensagem a ser enviada.

### Retorno
Nenhum. O método apenas atualiza o documento no banco de dados.
