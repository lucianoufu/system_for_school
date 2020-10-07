import ibm_db

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
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
except:
    print('Unable to conect: ', ibm_db.conn_errormsg())
