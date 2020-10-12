import ibm_db, logging, sys, os
import pandas as pd

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
        ,f_name VARCHAR(30)         NOT NULL
        ,l_name VARCHAR(30)         NOT NULL
    );'''

    create_query_parent = '''CREATE TABLE tb_parent
    (
        id            INTEGER
        ,f_name       VARCHAR(30) NOT NULL
        ,l_name       VARCHAR(30) NOT NULL
        ,address      VARCHAR(20) NOT NULL
        ,phone_number VARCHAR(12) NOT NULL
        ,id_son       INTEGER
        ,FOREIGN KEY (id_son) REFERENCES tb_student(id)
    );'''

    create_query_test1 = '''CREATE TABLE tb_test1
    (
        id_student         INTEGER
        ,note              NUMERIC(2,1) NOT NULL
        ,date_application  TIMESTAMP    NOT NULL
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
    



fn_db_table_creation()

students = {'ID': [], 'F_NAME': [], 'L_NAME': []}
opcao = input('Escolha uma opção: \n1 - Acessar como aluno/responsavel. \n2 - Acessar como professor. \n3 - Sair \nDigite: ')

if opcao == '1':
    show_student()
elif opcao == '2':
    print('Prof escolhido.')
elif opcao == '3':
    sys.exit()
elif opcao == 'adm':
    print('Welcome adm')
else:
    print('Opção invalida')

logging.debug('End program. \n\n')