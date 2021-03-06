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

def atualiza_filmes(conn,filme):
    """
    atualiza nome, data de lançamento e nota do filme
    :param conn:
    :param filme:
    :return filme id:
    """
    sql = '''UPDATE filmes
             SET nome = ?,
                 data_lancamento = ?,
                 nota= ?
             where id= ?'''
    cur = conn.cursor()
    cur.execute(sql,filme)

def deleta_filme(conn, id):
    """
    Deleta o filme por id
    :param conn: Conexão na base de dados
    :param id:id do filme
    """
    sql = 'DELETE FROM filmes WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql,(id,))

def deleta_todos_filmes(conn):
    """
    Deleta todas as linhas na tabela de filmes
    :param conn: Conexão na base de dados
    :return:
    """
    sql = 'DELETE FROM filmes'
    cur = conn.cursor()
    cur.execute(sql)

def seleciona_filmes(conn):
    """
    Busca todas as linhas na tabela de filmes
    :paramentro conn:Objeto de conexão
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM filmes")

    rows = cur.fetchall()
    print("==================Catálogo================")

    for row in rows:
        print(row)
    print("==========================================")

def main():
    #base de dados que utilizaremos
    database = 'pythonsqlite.db'
    #variavel recebe o script para criação da tabela de filmes
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
        #Menu com as opções para o usuario
        opcao = ""
        while(opcao != 0):
            print("++++++++++++++++MENU++++++++++++++++")
            opcao = int(input("1-Mostrar catálogo\n2-Adicionar filme\n3-Atualizar filme\n4-Deletar filmes\n0-Sair\nDigite o codigo da opção desejada:"))
            if opcao == 1:
                seleciona_filmes(conn)
            elif opcao == 2:
                #cria novo filme
                nome = input("Digite o nome do filme:\n")
                data_lancamento = input("Digite a data do filme(yyyy-mm-dd):\n")
                nota = input("Digite a nota do filme(0-10):\n")
                filme = (nome, data_lancamento, nota)
                filme_id = cria_filme(conn, filme)
                print (filme_id)
            elif opcao ==3:
                #atualiza filme
                filme_id = int(input("Digite o id do filme que deseja atualizar:\n"))
                nome = input("Digite o nome do filme:\n")
                data_lancamento = input("Digite a data do filme(yyyy-mm-dd):\n")
                nota = input("Digite a nota do filme(0-10):\n")
                atualiza_filmes(conn,(nome,data_lancamento,nota,filme_id))
            elif opcao == 4:
                opcao = int(input("1-Deletar filme por ID\n2-Deletar todo o catálogo\n0-Sair\nDigite o codigo da opção desejada:")) 
                if opcao == 1:
                    filme_id = int(input("Digite o id do filme que deseja deletar: "))
                    deleta_filme(conn, filme_id)
                elif opcao==2:
                    deleta_todos_filmes(conn)
                else:
                    print("See Ya!")
            else:
                print("See Ya!!")


if __name__ =='__main__':
    main()
    