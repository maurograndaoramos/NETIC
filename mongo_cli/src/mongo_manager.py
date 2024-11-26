from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from datetime import datetime

class mongo_remote_db :
    def __init__ (self) :
        # Conectar ao mongodb
        uri = "mongodb+srv://admin:123@chatapp.0ej6v.mongodb.net/?retryWrites=true&w=majority&appName=chatApp"
        client = MongoClient(uri, server_api=ServerApi('1'))

        # nome do banco de dados e banco de dados que vai ser usado
        db_name = "chat_db"
        db = client[db_name]

        # nome da colecao vai ser usado
        chat_collection_name = "chats"

        # criar colecao que vai ser usada, caso n exista
        if chat_collection_name not in db.list_collection_names(): 
            db.create_collection(chat_collection_name)
        
        # definir o acesso global a colecao que vai ser usada
        self.chat_collection = db[chat_collection_name]

    # funcao para ter todos os chats
    def get_all_chats (self) :
        # buscar todos os os chats que tem no banco de dados
        all_chats = self.chat_collection.find()

        # all chats ira retornar isso abaixo
        # <pymongo.synchronous.cursor.Cursor object at 0x7fc7fbb2cec0>
        # o array all_chats_readable vai ser criado para uma melhor visualizacao, uma vez que o valor acima tmb pode ser interado
        # WARNING : as proximas 3 linhas de codigo e para e unicamente visual, pode ser retirado e adicionado apenas 
        # return all_chats 
        
        # array para adicionar os chats de forma legivel
        all_chats_readable = []
        
        # loop por todos os chats para adicionar de na array para os tornar legiveis
        for chat in all_chats :
            all_chats_readable.append(chat)

        # retorna os chats de forma visivel 
        return all_chats_readable

    # funcao para pegar todas as menssagens de um chat (pelo id)
    def get_messages(self, chat_id) :
        nid = ObjectId(chat_id)
        
        # pega o chat
        actual_chat = self.chat_collection.find({"_id" : nid})[0]

        # retorna as menssagens
        return actual_chat['messages']
    
    # funcao para buscar todos os chats de um user
    def get_chats(self, user_id) :
        # buscar todos os chats do banco de dados
        all_chats = self.get_all_chats()
    
        # array vazia que vai armazenar os chats em que o usuario esta
        chats_with_user = []
        
        # loop por todos os chats
        for chat in all_chats:
            # pegar os usuarios que estao neste chat
            users_in_chat = chat['users']

            if str(user_id) in users_in_chat : # caso o usuario esteja neste chat
                chats_with_user.append(chat)

        # retorna todos os usuarios em que o usuario esta
        return chats_with_user

    # funcao para buscar ou criar chat caso n exista
    def get_or_create_chat(self, user_id=None, friend_id=None, chat_id=None) :
        if not chat_id : # caso n seja fornecido chat_id
            
            chat = self.chat_collection.find_one({"users": {"$all": [user_id, friend_id]}})

            if not chat:
                new_chat = {
                    "users": [user_id, friend_id],
                    "messages": []  # Inicializa o chat com uma lista de mensagens vazia
                }
                # Insere o novo chat na coleção
                chat_id = self.chat_collection.insert_one(new_chat).inserted_id
                # Busca o chat recém-criado para garantir retorno consistente
                chat = self.chat_collection.find_one({"_id": chat_id})

            return chat
        else : # caso forneca o chat_id
            # transforma ele um obj id
            nid = ObjectId(chat_id)

            # caso exista um chat com esse id, retorn ele
            return self.chat_collection.find_one({"_id" : nid})

    # duncao para add uma menssagem
    def add_message(self, chat_id, user_id, msg_content) :
        # buscar o chat pelo chat id
        actual_chat = self.get_or_create_chat(chat_id=chat_id)
        
        # buscar hora e minuo
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # criar obj da msg
        message_obj = {
            "user_id" : user_id,
            "content" : msg_content,
            "sent_time" : f"{hour}:{minute}"
        }

        # tansformar id em obj id
        nid = ObjectId(chat_id)

        # push na menssagem
        self.chat_collection.update_one (
            {"_id" : nid}, 
            {"$push" : {"messages" : message_obj}}
        )