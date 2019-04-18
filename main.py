import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    #cria uma conexão com a base de dados SQLite
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    """cria tabela 
    :param conn: objeto conexao
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    
def cria_filme(conn,filme):
    """
    Cria um novo filme na tabela de filmes
    :param conn:
    :param filme:
    :return: filme id
    """
    sql ='''INSERT INTO filmes(nome,data_lancamento,nota)
            VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, filme)
    return cur.lastrowid

def main():
    database = 'pythonsqlite.db'
    #variavel recebe o script para criação da tabela
    sql_cria_tabela_filmes = """ CREATE TABLE IF NOT EXISTS filmes (
                                        id integer PRIMARY KEY,
                                        nome text NOT NULL,
                                        data_lancamento text,
                                        nota int
                                    ); """

    #cria conexão com base de dados
    conn = create_connection(database)
    if conn is not None:
        #cria a tabela de projetos
        create_table(conn, sql_cria_tabela_filmes)
    else:
        print("Erro ! Não foi possivel estabelecer uma conexão com a base de dados")

    with conn:
        #cria novo filme
        nome = input("Digite o nome do filme:\n")
        data_lancamento = input("Digite a data do filme(yyyy-mm-dd):\n")
        nota = input("Digite a nota do filme(0-10):\n")
        filme = (nome, data_lancamento, nota)
        filme_id = cria_filme(conn, filme)
        print (filme_id)
            


if __name__ =='__main__':
    main()
    