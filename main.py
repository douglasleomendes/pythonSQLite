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
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_task(conn,task):
    """
    Cria nova tarefa
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql,task)
    return cur.lastrowid
    
def create_project(conn,project):
    """
    Cria um novo projeto na tabela de projetos
    :param conn:
    :param project:
    :return: project id
    """
    sql ='''INSERT INTO projects(name,begin_date,end_date)
            VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def main():
    database = 'pythonsqlite.db'

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    #cria conexão com base de dados
    conn = create_connection(database)
    if conn is not None:
        #cria a tabela de projetos
        create_table(conn, sql_create_projects_table)
        #cria tabela de tarefas
        create_table(conn, sql_create_tasks_table)
    else:
        print("Erro ! Não foi possivel estabelecer uma conexão com a base de dados")

    opcao = input('Digite a opção desejada:\n1-Adicionar Projeto\n2-Adicionar Tarefa')
    if opcao == 1:
        with conn:
            #cria novo projeto
            project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
            project_id = create_project(conn, project)
            #tarefas
            task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
            task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
            #cria tarefas
            create_task(conn, task_1)
            create_task(conn, task_2)




if __name__ =='__main__':
    main()
    