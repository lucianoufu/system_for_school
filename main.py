import ibm_db, logging, sys, os


## Logging configuration
logging.basicConfig(filename = 'debug.txt', level = logging.DEBUG, format = '%(levelname)s - %(asctime)s - %(message)s')
logging.debug('Begin program.')

## Data base creadential's
logging.info('Data base connection:')
dsn_driver   = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_hostname = "dashdb-txn-sbox-yp-dal09-08.services.dal.bluemix.net"
dsn_port     = 50000
dsn_protocol = "TCPIP"
dsn_uid      = "nsj92075"
dsn_pwd      = "2kmb5j-q1k6d927s"
dsn = (
    "DRIVER = {0};"
    "DATABASE = {1};"
    "HOSTNAME = {2};"
    "PORT = {3};"
    "PROTOCOL = {4};"
    "UID = {5};"
    "PWD = {6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

try:
    conn = ibm_db.connect(dsn, "", "")
    logging.debug('Connection to database: {} as user on host {}'.format(dsn_database, dsn_uid, dsn_hostname))
except:
    logging.critical('Unable to connect {} on host {}'.format(dsn_database, dsn_hostname))

def fn_db_table_creation():
    create_query_student = '''CREATE TABLE tb_student
    (
        id     INTEGER PRIMARY KEY NOT NULL
        ,f_name VARCHAR(30)        NOT NULL
        ,l_name VARCHAR(30)        NOT NULL
        ,class                     VARCHAR(5)
        ,password                  VARCHAR(20)
    );'''

    create_query_teacher = '''CREATE TABLE tb_teacher
    (
        id INTEGER PRIMARY KEY NOT NULL
        ,f_name   VARCHAR(30)
        ,l_name   VARCHAR(30)
        ,password VARCHAR(30)
    )'''

    create_query_test1 = '''CREATE TABLE tb_test1
    (
        id_student         INTEGER
        ,id_teacher        INTEGER
        ,discipline        VARCHAR(30)
        ,note              NUMERIC(3,1) NOT NULL
        ,date_application  TIMESTAMP    NOT NULL
        ,class             VARCHAR(10)
        ,FOREIGN KEY (id_student) REFERENCES tb_student(id)
        ,FOREIGN KEY (id_teacher) REFERENCES tb_teacher(id)
    );'''

    create_query_test2 = '''CREATE TABLE tb_test2
    (
        id_student         INTEGER
        ,id_teacher        INTEGER
        ,discipline        VARCHAR(30)
        ,note              NUMERIC(3,1) NOT NULL
        ,date_application  TIMESTAMP    NOT NULL
        ,class             VARCHAR(10)
        ,FOREIGN KEY (id_student) REFERENCES tb_student(id)
        ,FOREIGN KEY (id_teacher) REFERENCES tb_teacher(id)
    );'''

    create_query_test3 = '''CREATE TABLE tb_test3
    (
        id_student         INTEGER
        ,id_teacher        INTEGER
        ,discipline        VARCHAR(30)
        ,note              NUMERIC(3,1) NOT NULL
        ,date_application  TIMESTAMP    NOT NULL
        ,class             VARCHAR(10)
        ,FOREIGN KEY (id_student) REFERENCES tb_student(id)
        ,FOREIGN KEY (id_teacher) REFERENCES tb_teacher(id)        
    );'''

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_student)
        logging.debug('Table tb_student created.')
    except:
        logging.error('Table tb_student already exists or the query has an error')

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_teacher)
        logging.debug('Table tb_teacher created.')
    except:
        logging.error('Table tb_parent alreadt exists or the query has an error.')

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_test1)
        logging.debug('Table tb_test1 created.')
    except:
        logging.error('Table tb_test1 already exists or the query has an error.')

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_test2)
        logging.debug('Table tb_test2 created.')
    except:
        logging.error('Table tb_test2 already exists or the query has an error.')

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_test3)
        logging.debug('Table tb_test3 created.')
    except:
        logging.error('Table tb_test3 already exists or the query has an error.')

def fn_loging(name):
    print()
    while True:
        f_name = input('Digite seu nome: ').title()
        l_name = input('Digite seu sobrenome: ').title()
        password = input('Digite a sua senha: ')
        sql = "SELECT * FROM tb_{} WHERE f_name = '{}' and l_name = '{}' and password = '{}'".format(name, f_name, l_name, password)
        stmt = ibm_db.exec_immediate(conn, sql)
        tuple_sql = ibm_db.fetch_tuple(stmt)
        if tuple_sql == False:
            print('Usuário ou senha incorreto.')
        elif name == 'student':
            fn_show_notes(tuple_sql[0])
            break
        elif name == 'teacher':
            fn_teacher_options(tuple_sql[0])

def fn_show_notes(id_db):
    sql = '''SELECT s.f_name as studant_name
    ,t.f_name as teacher_name
    ,p1.note as p1_note
    ,p1.class as class
    ,p2.note as p2_note
    ,p2.class as class
    ,p3.note as p3_note
    ,p3.class as class
    FROM 
    tb_student as s
    INNER JOIN
    (
        tb_test1 as p1
        INNER JOIN 
        (
        	tb_test2 as p2 
        	INNER JOIN 
        	(
        		tb_test3 as p3 
        		INNER JOIN tb_teacher as t
        		ON t.id = p3.id_teacher
        	)
        	ON p2.id_teacher = t.id
        )
        ON p1.id_teacher = t.id
    )
    ON p1.id_student = s.id;

    WHERE s.id = {}
    ORDER BY p1.class DESC;
    '''.format(id_db)
    stmt = ibm_db.exec_immediate(conn, sql)
    tuple_sql = ibm_db.fetch_tuple(stmt)
    while tuple_sql != False:
        print('\nAluno: {} \nProfessor: {} \nNota P1: {} classe: {} \nNota P2: {}, classe: {} \nNota P3: {}, classe: {}.\n'.format(tuple_sql[0], tuple_sql[1], tuple_sql[2], tuple_sql[3], tuple_sql[4], tuple_sql[5], tuple_sql[6], tuple_sql[7]))
        tuple_sql = ibm_db.fetch_tuple(stmt)
            
def fn_teacher_options(id_db_teacher):
    opcao = input('Escolha uma opção: 1 - Lançar notas. 2 - Voltar ao menu. \nDigite: ')
    if opcao == '1':
        discipline    = input('Digite o nome da disciplina: ')
        clas_s = input('Digite a classe no qual a prova foi aplicada: ')

        while True:
            opcao = input('1 - Lançar notas da 1ª prova. \n2 - Lançar notas da 2ª prova. \n3 - Lançar notas da 3ª prova \n4 - Voltar ao menu. \nDigite: ')
            if opcao == '1':
                fn_send_notes(1, id_db_teacher, discipline, clas_s)
            elif opcao == '2':
                fn_send_notes(2, id_db_teacher, discipline, clas_s)
            elif opcao == '3':
                fn_send_notes(3, id_db_teacher, discipline, clas_s)
            elif opcao == '4':
                #>>>>> Opção não está retornando ao menu <<<<<<<<<<<<
                break
    else:
        print('Opcao invalida')

def fn_send_notes(test, id_db_teacher, discipline, clas_s):
    while True:
        date = input('Digite o dia que a prova foi aplicada: ')
        f_name        = input('Digite o nome do aluno: ')
        l_name        = input('Digite o sobrenome do aluno: ')
        sql = "SELECT * FROM tb_student WHERE f_name = '{}' AND l_name = '{}'".format(f_name, l_name)
        stmt = ibm_db.exec_immediate(conn, sql)
        tuple_sql = ibm_db.fetch_tuple(stmt)
        if tuple_sql == False:
            print('Aluno invalido:')
        else:
            id_db = tuple_sql[0]
            break
    note = input('Digite a nota da {}ª prova: '.format(test))
    sql = "INSERT INTO tb_test{} VALUES ({}, {},'{}' ,{}, '{}', '{}');".format(test, id_db, id_db_teacher, discipline, note, date, clas_s)
    stmt = ibm_db.exec_immediate(conn, sql)
    print('Nota lançada com sucesso')

def fn_adm_options():
    opcao = input('\n\nEscolha uma opção: \n1 - Inserir aluno. \n2 - Deletar aluno. \n3 - Atualizar dados de um aluno. \n4 - Inserir professor. \n5 - Deletar professor \n6 - Atualizar professor. \nDigite: ')
    if opcao == '1':
        fn_insert('student')
    elif opcao == '2':
        fn_delete('student')
    elif opcao == '3':
        fn_update('student')
    elif opcao == '4':
        fn_insert('teacher')
    elif opcao == '5':
        fn_delete('teacher')
    elif opcao == '6':
        fn_update('teacher')
    else:
        print('Opção invalida.')

def fn_insert(name):
    if name == 'student':
        name_pt = 'aluno'
    elif name == 'teacher':
        name_pt = 'professor'
    id_db = input('Digite o id do {}: '.format(name_pt))
    f_name = input('Digite o nome do {}: '.format(name_pt))
    l_name = input('Digite o sobrenome do {}: '.format(name_pt))
    password = input('Digite a senha do {}: '.format(name_pt))
    if name == 'student':
        clas_s = input('Digite a classe do {}: '.format(name_pt))
        sql = '''INSERT INTO ''' + 'tb_' + name + ''' 
        (
        id
        ,f_name
        ,l_name
        ,class
        ,password
        )
        VALUES
        ({}, '{}', '{}', '{}', '{}');'''.format(id_db, f_name, l_name, clas_s, password)
    else:
        sql = '''INSERT INTO tb_{}
        (
        id
        ,f_name
        ,l_name
        ,password
        )
        VALUES
        ({}, '{}', '{}', '{}');'''.format(name, id_db, f_name, l_name, password)
    
    
    stmt = ibm_db.exec_immediate(conn, sql)
    try:
        if name == 'student':
            logging.debug('Value ({}, {}, {}, {},{}); insert into tb_{}.'.format(id_db, f_name, l_name, clas_s, password, name))
            print('{} inserido com sucesso.\n\n'.format(name_pt))
        else:
            print('{} inserido com sucesso.\n\n'.format(name_pt))
            logging.debug('Value ({}, {}, {}, {}); insert into tb_{}.'.format(id_db, f_name, l_name, password, name))
    except:
        print('{} não inserido.\n'.format(name_pt))
        if name == 'student':
            logging.error('Value ({}, {}, {}, {},{}); not insert into tb_{}.'.format(id_db, f_name, l_name, clas_s, password, name))
        else:
            print('{} não inserido.\n'.format(name_pt))
            logging.error('Value ({}, {}, {}); not insert into tb_{}.'.format(id_db, f_name, l_name, name))

def fn_delete(name):
    #Teste para comentário
    if name == 'student':
        name_pt = 'Aluno'
    else:
        name_pt = 'Professor'
    
    while True:
        opcao = input('Escolha uma opção: \n1 - Deletar pelo id. \n2 - Deletar pelo nome. \n3 - Voltar ao menu. \nDigite: ')
        if opcao == '1':
            try:
                id_db = input('Digite o id do {}: '.format(name_pt))
                sql_select = 'SELECT * FROM tb_{} WHERE id = {}'.format(name, id_db)
                sql = 'DELETE FROM tb_{} WHERE id = {}'.format(name, id_db)
                stmt = ibm_db.exec_immediate(conn, sql_select)
                tuple_select = ibm_db.fetch_tuple(stmt)
                stmt = ibm_db.exec_immediate(conn, sql)
                logging.debug('Value deleted from tb_{}!! Value: {}'.format(name, tuple_select))
                print('Valor deletado com sucesso\n\n')
                break
            except:
                logging.error('Id {} not deleted from tb_{}'.format(id_db, name))
                print('Valor não deletado!\n')
        elif opcao == '2':
            try:
                f_name = input('Digite o primeiro nome: ')
                l_name = input('Digite o sobrenome: ')
                sql = "DELETE FROM tb_{} WHERE f_name = '{}' and l_name = '{}'".format(name, f_name, l_name)
                sql_select = "SELECT * FROM tb_{} where f_name = '{}' and l_name = '{}'".format(name, f_name, l_name)
                stmt = ibm_db.exec_immediate(conn, sql_select)
                tuple_select = ibm_db.fetch_tuple(stmt)
                print('Valor deletado com sucesso\n\n')
                logging.debug('Value deleted from tb_{}!! Value: {}'.format(name, tuple_select))
                break
            except:
                print('Valor não deletado \n')
                logging.erro('Value with f_name = {} and l_name {} not deleted from tb_{}.'.format(f_name, l_name, name))
        elif opcao == '3':
            break
        else:
            print('Opção invalida.')

def fn_update(name):
    if name == 'student':
        name_pt = 'Aluno'
    else:
        name_pt = 'Professor'

    while True:
        id_db = input('Digite o id do {}: '.format(name_pt))
        sql_select = 'SELECT * FROM tb_{} WHERE id = {}'.format(name, id_db)
        stmt = ibm_db.exec_immediate(conn, sql_select)
        old_values = ibm_db.fetch_tuple(stmt)
        sql_select = 'SELECT * FROM tb_{} WHERE id = {}'.format(name, id_db)
        stmt = ibm_db.exec_immediate(conn, sql_select)
        tuple_select = ibm_db.fetch_tuple(stmt)

        id_db = input('Digite o novo id: {} -> (enter para manter o id): '.format(tuple_select[0]))
        if id_db == '':
            id_db = old_values[0]
        f_name = input('Digite o novo primeiro nome: {} -> (enter para manter o primeiro nome): '.format(tuple_select[1]))
        if f_name == '':
            f_name = old_values[1]
        l_name = input('Digite o novo sobrenome: {} -> (enter para manter o sobrenome): '.format(tuple_select[2]))
        if l_name == '':
            l_name = old_values[2]
        if name == 'student':
            clas_s = input('Digite a nova classe: {} -> (enter para manter a classe): '.format(tuple_select[3]))
            if clas_s == '':
                clas_s = old_values[3]
            password = input('Digite a nova senha: {} -> (enter para manter a mesma senha): '.format(tuple_select[4]))
            if password == '':
                password = old_values[4]
            sql = '''UPDATE tb_{} 
            SET id = {}
            ,f_name = '{}'
            ,l_name = '{}'
            ,class = '{}'
            ,password = '{}' 
            WHERE id = {}'''.format(name, id_db, f_name, l_name, clas_s, password, id_db)
        else:
            sql = '''UPDATE tb_{} 
            SET id = {}
            ,f_name = '{}'
            ,l_name = '{}'
            WHERE id = {}'''.format(name, id_db, f_name, l_name, id_db)

        try:
            stmt = ibm_db.exec_immediate(conn, sql)
            print('Valor atualizado com sucesso.\n\n')
            if name == 'student':
                logging.debug('Values update tb_{} {} -> ({}, {}, {}, {}, {})'.format(name, old_values, id_db, f_name, l_name, clas_s, password))
            else:
                logging.debug('Values update tb_{} {} -> ({}, {}, {})'.format(name, old_values, id_db, f_name, l_name))
            break
        except:
            print('Valor não atualizado.')
            logging.error('Table tb_{} not update.'.format(name))

fn_db_table_creation()

students = {'ID': [], 'F_NAME': [], 'L_NAME': []}
while True:
    opcao = input('Escolha uma opção: \n1 - Acessar como aluno/responsavel. \n2 - Acessar como professor. \n3 - Sair \nDigite: ')

    if opcao == '1':
        fn_loging('student')
    elif opcao == '2':
        fn_loging('teacher')
    elif opcao == '3':
        logging.debug('End program. \n\n')
        sys.exit()
    elif opcao == 'adm':
        fn_adm_options()
    else:
        print('Opção invalida')

logging.debug('End program. \n\n')