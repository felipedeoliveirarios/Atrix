import sys
import sqlite3

database = 'atrix.db'

# Cria uma base de dados SQLite para armazenar informações, caso não exista.
def loadDB():
    # Conecta ao banco de dados no arquivo Atrix.
    connection = sqlite3.connect(database)
    # Cria um cursor do banco de dados, que é um iterador que permite navegar
    # e manipular os registros do bd, e o atribui a uma variável.
    cursor = connection.cursor()
    # Carrega os comandos a partir do script sql
    script = open('create.sql', 'r').read()
    # Executa os comandos do script SQL diretamente no banco de dados.
    cursor.executescript(script)
    # Salva as alterações.
    connection.commit()
    # Encerra a conexão.
    connection.close()

# Confere se o usuário já tem uma ficha criada.
def checkuser(user_id, group_id):
    # Conecta ao banco de dados no arquivo Atrix.
    connection = sqlite3.connect(database)
    # Cria um cursor do banco de dados, que é um iterador que permite navegar
    # e manipular os registros do bd, e o atribui a uma variável.
    cursor = connection.cursor()
    if len(cursor.executescript(''' SELECT Id_Grupo, Id_Jogador
                                    FROM FICHAS
                                    WHERE Id_Grupo = ? AND Id_Jogador = ?''',
                                user_id, group_id) > 0):
        return True
    else:
        return False

