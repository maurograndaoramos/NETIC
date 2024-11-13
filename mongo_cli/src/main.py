from InquirerPy import inquirer
from mongo_manager import mongo_remote_db

from os import system
mongo_db = mongo_remote_db()

def script () :
    system("clear")

    opcao_principal = inquirer.select(
        message="Selecione o que queres testar",
        choices=[
            "ver todos os chats",
            "ver todos os chats de um usuario",
            "ver um chat especifico de um usuario ou por uma id especifica",
            "ver menssagens de um chat",
            "adicionar uma menssagem a um chat"
        ]
    ).execute()

    # se quiser ver todos os chats
    if opcao_principal == "ver todos os chats" :
        # buscar todos os chats
        all_chats = mongo_db.get_all_chats()
        print("todos os chats existentes no banco de dados")
        print(all_chats)

    # se quiser ver um chat especifico (entre users ou por id)
    elif opcao_principal == "ver um chat especifico de um usuario ou por uma id especifica" :
        # opcao de bisca
        opcao_de_busca = inquirer.select(
            message="Qual o metodos be busca do chat",
            choices= [
                "Busca pelo Id do chat",
                "Busca pelos id dos usuarios",
            ]
        ).execute()

        # caso queira buscar pelo id
        if opcao_de_busca == "Busca pelo id do chat" :
            print("Caso n exista chat com esse id, ele NAO vai ser criado !")
            # pega o id e busca o chat pela id
            chat_id = inquirer.text(message="Qual id do char para procurar ?").execute()
            chat_with_id = mongo_db.get_or_create_chat(chat_id=chat_id)
            print(chat_with_id)

        # caso queira buscar por ids de 2 usuarios
        elif opcao_de_busca == "Busca pelos id dos usuarios" :
            print("Caso n exista chat entere esses usuario, ele vai ser criado !")
            # pegar id dos usuarios
            user_id_one = inquirer.text(message="Qual id do usario 1 ?").execute()
            user_id_two = inquirer.text(message="Qual id do usario 2 ?").execute()

            # pega o chat com os dois users, caso n exista crie
            chats_with_users = mongo_db.get_or_create_chat(
                user_id=user_id_one,
                friend_id= user_id_two
            )

            print(chats_with_users)

    # se quiser ver todos os chats que um usuario tem
    elif opcao_principal == "ver todos os chats de um usuario" :
        # capta a id do usurio que quer ver o chat
        user_id = inquirer.text(message="Qual id do usario que quer ver os chats ?").execute()

        # busca no mongo os chats que o user tem (a busca e feita com o id)
        user_id_chats = mongo_db.get_chats(user_id=user_id)

        if len(user_id_chats) > 0 : # se a quantidade de chats for maior que 0
            print ("os chats que o usuario tem :")
            print (user_id_chats)
        else : # se n tiver chats
            print("o usuario ainda n tem chats")
            print (user_id_chats)

    # caso queira ver as menssagens de um chat
    elif opcao_principal == "ver menssagens de um chat" :
        chat_id = inquirer.text(message="Qual id do chat para ver todas as msgs ?").execute()
        print (f"Menssagen do chat com id : {chat_id}")
        messages_from_chat = mongo_db.get_messages(chat_id=chat_id)
        print (messages_from_chat)

    # caso queira add uma menssagem a um chat pelo id
    if opcao_principal == "adicionar uma menssagem a um chat" :
        # pega as info da menssagem
        chat_id = inquirer.text(message="Qual id do chat para add a msg ?").execute()
        user_id = inquirer.text(message="Qual id do user que vai enviar ?").execute()
        msg_content = inquirer.text(message="Qual a menssagem ?").execute()

        # add a msg
        mongo_db.add_message(chat_id=chat_id, user_id=user_id, msg_content=msg_content)
    
    confirm = inquirer.confirm(message="continuar ?").execute()
    script()

script()