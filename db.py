import firebirdsql

from collections import namedtuple

USER = 'SYSDBA'
PASSWORD = 'masterkey'
CONNECTION_STRING = '192.168.1.5:C:\\Users\\smocnik\\AppData\\Roaming\\OEvent\\Data\\Competition10.gdb'

SELECT_COMPETITORS = 'SELECT * FROM OEVLISTSVIEW'
SELECT_COMPETITION_DATA = 'SELECT * FROM OEVCOMPETITION'

# cur.describe
# (name, type_code, display_size, internal_size, precision, scale, null_ok)

def get_data(connection_string):
    conn = firebirdsql.connect(dsn=connection_string, user=USER, password=PASSWORD)
    competition = get_table(conn, "OEVCOMPETITION")
    competitors = get_table(conn, "OEVLISTSVIEW")
    conn.close()
    return competition, competitors


def get_table(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s" % table)
    data = cur.fetchall()
    desc = [description[0] for description in cur.description]
    cur.close()
    table_class = namedtuple(table, desc)
    return [table_class(*row) for row in data]
