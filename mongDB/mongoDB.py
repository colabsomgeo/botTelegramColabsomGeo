from pymongo import MongoClient, errors

uri = 'mongodb+srv://carvalhosannyer:hM5H1hdxMZ7x9mTL@cluster0.feb5b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
db = 'colabSomGeo'
user_colletion = 'user'
som_colletion = 'captura_som'
captura_som_colletion = "captura_som"


def connection(uri, database, collection):
    try:
        # Tentativa de conexão com o servidor MongoDB
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Verifica se a conexão foi bem-sucedida
        client.admin.command('ping')
        print("Conectado ao MongoDB com sucesso!")
        
        # Acessa o banco de dados e a coleção especificados
        db = client[database]
        colecao = db[collection]
        return colecao
    
    except errors.ServerSelectionTimeoutError:
        print("Erro: Não foi possível conectar ao servidor MongoDB. Verifique a URI e o servidor.")
    except errors.ConnectionFailure:
        print("Erro: Falha na conexão com o MongoDB.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    return None


def salvarUser(telegram_id, nome):
    collection = connection(uri, db, user_colletion)
    documento = {"telegram_id": telegram_id, "nome": nome}
    
    if collection is not None:  # Comparação explícita com None
        try:
            # Tenta inserir o documento na coleção
            resultado = collection.insert_one(documento)
            print(f"Usuário salvo com sucesso! ID: {resultado.inserted_id}")
            return resultado.inserted_id
        except Exception as e:
            # Captura erros relacionados à inserção
            print(f"Erro ao inserir o documento: {e}")
    else:
        print("Falha ao conectar à coleção.")

def acharUser(telegram_id):
    collection = connection(uri, db, user_colletion)
    if collection is not None:
        try:
            documento = collection.find_one({"telegram_id": telegram_id})
          
    
            if documento:
                print(f"Usuário encontrado: {documento}")
                return documento.get("_id")
             
            else:
                print("Usuário não encontrado.")
                return 0
        except Exception as e:
            print(f"Erro ao buscar o documento: {e}")
    else:
        print("Falha ao conectar à coleção.")

def salvarInfoAudio(dadosAudio):
    collection = connection(uri, db, som_colletion)
    if collection is not None:
        try:
            resultado = collection.insert_one(dadosAudio)
            print(f"Dados do áudio salvo com sucesso! ID: {resultado.inserted_id}")
        except Exception as e:
             print(f"Erro ao inserir o documento: {e}")
    else:
        print("Falha ao conectar à coleção.")