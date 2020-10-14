import ibm_db, logging, sys, os


## Logging configuration
logging.basicConfig(filename = 'debug.txt', level = logging.DEBUG, format = '%(levelname)s - %(asctime)s - %(message)s')
logging.debug('Begin program.')

logging.info('Data base connection:')
## Data base creadential's
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

    #create_query_parent = '''CREATE TABLE tb_parent
    #(
    #    id            INTEGER
    #    ,f_name       VARCHAR(30) NOT NULL
    #    ,l_name       VARCHAR(30) NOT NULL
    #    ,address      VARCHAR(20) NOT NULL
    #    ,phone_number VARCHAR(12) NOT NULL
    #    ,id_son       INTEGER
    #    ,FOREIGN KEY (id_son) REFERENCES tb_student(id)
    #);'''

    create_query_test1 = '''CREATE TABLE tb_test1
    (
        id_student         INTEGER
        ,note              NUMERIC(2,1) NOT NULL
        ,date_application  TIMESTAMP    NOT NULL
        ,class             NUMERIC(2,1)
        ,FOREIGN KEY (id_student) REFERENCES tb_student(id)
    );'''

    create_query_test2 = '''CREATE TABLE tb_test2
    (
        id_student        INTEGER
        ,note             NUMERIC(2,1) NOT NULL
        ,date_application TIMESTAMP    NOT NULL
        ,FOREIGN KEY (id_student) REFERENCES tb_student(id)
    );'''

    create_query_test3 = '''CREATE TABLE tb_test3
    (
        id_student        INTEGER
        ,note             NUMERIC(2,1) NOT NULL
        ,date_application TIMESTAMP    NOT NULL
        ,FOREIGN KEY (id_student) REFERENCES tb_student(id)
    );'''

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_student)
        logging.debug('Table tb_student created.')
    except:
        logging.error('Table tb_student already exists or the query has an error')

    try:
        create_stmt = ibm_db.exec_immediate(conn, create_query_parent)
        logging.debug('Table tb_parent created.')
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

def fn_student_loging():
    print()
    while True:
        f_name = input('Digite o nome do aluno: ').title()
        senha = input('Digite a sua senha: ')
        sql = 'select * from tb_student where f_name = ' + f_name + ' and keyword = ' + senha + ';'
        stmt = ibm_db.exec_immediate(conn, sql)
        dictonary = ibm_db.fetch_tuple(stmt)
        if dictonary == ():
            print('Usuário ou senha incorreto.')
        else:
            ###########################################################################
            #
            #>>>>>>>>>>>>>>>>>>>>>> Continue here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            #
            ###########################################################################
            print('Usuário e senha estão corretos :).')
            #fn_student_show_note()

#def fn_student_show_note(name):
#    sql = '''
#    SELECT p1.note
#          ,p2.note
#          ,p3.note
#    FROM tb_note1
#    INEER JOIN
#    (
#        tb_note2 as p2
#        INNER JOIN tb_note3 as p3
#        ON p3.id = p2.id
#    )
#    ON p2.id = p1.id'''
#    stmt = ibm_db.exec_immediate(conn, sql)
#    dict = ibm_db.fetch_assoc(stmt)
#    print(dict)


def show_student():
    sql = 'SELECT * FROM tb_student'
    stmt = ibm_db.exec_immediate(conn, sql)
    dictonary = ibm_db.fetch_assoc(stmt)
    while (dictonary) != False:
        students['ID'].append(dictonary['ID'])
        students['F_NAME'].append(dictonary['F_NAME'])
        students['L_NAME'].append(dictonary['L_NAME'])
        dictonary = ibm_db.fetch_assoc(stmt)
    student_df = pd.DataFrame(students)
    print(student_df.loc[:, ['F_NAME', 'L_NAME']])
    fn_student_loging()

def fn_adm_options():
    opcao = input('\n\nEscolha uma opção: \n1 - Inserir aluno. \n2 - Deletar aluno. \n3 - Atualizar dados de um aluno. \n4 - Inserir professor. \n5 - Deletar professor \n6 - Atualizar professor. \nDigite: ')
    if opcao == '1':
        fn_insert('student')

def fn_insert(name):
    if name == 'student':
        name_pt = 'aluno'
    elif name == 'teacher':
        name_pt = 'professor'
    id_student = input('Digite o id do {}: '.format(name_pt))
    f_name = input('Digite o nome do {}: '.format(name_pt))
    l_name = input('Digite o sobrenome do {}: '.format(name_pt))
    clas_s = input('Digite a classe do {}: '.format(name_pt))
    password = input('Digite a senha do {}: '.format(name_pt))
    sql = '''INSERT INTO ''' + 'tb_' + name + ''' 
    (id
    ,f_name
    ,l_name
    ,class
    ,password
    )
    VALUES
    ('{}', '{}', '{}', '{}', '{}');'''.format(id_student, f_name, l_name, clas_s, password)
    
    try:
        stmt = ibm_db.exec_immediate(conn, sql)
        logging.debug('Value (' + id_student + ', ' + f_name + ', ' + l_name + ', ' + clas_s + ', ' + password + '); insert into tb_student.')
    except:
        print('Valor não inserido.')
        logging.error('Value (' + id_student + ', ' + f_name + ', ' + l_name + ', ' + clas_s + ', ' + password + '); not insert into tb_student.')



fn_db_table_creation()

students = {'ID': [], 'F_NAME': [], 'L_NAME': []}
opcao = input('Escolha uma opção: \n1 - Acessar como name/responsavel. \n2 - Acessar como professor. \n3 - Sair \nDigite: ')

if opcao == '1':
    show_student()
elif opcao == '2':
    print('Prof escolhido.')
elif opcao == '3':
    sys.exit()
elif opcao == 'adm':
    fn_adm_options()
else:
    print('Opção invalida')

logging.debug('End program. \n\n')