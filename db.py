""" Module connecting to OEVENT Firebird SQL database and exporting competition data. """
from collections import namedtuple

import firebirdsql

USER = 'SYSDBA'
PASSWORD = 'masterkey'

def get_data(connection_string):
    """ Get competition data from firebird sql database at `connection_string`. """
    conn = firebirdsql.connect(dsn=connection_string, user=USER, password=PASSWORD)
    try:
        competition = get_table(conn, "OEVCOMPETITION")
        competitors = get_table(conn, "OEVLISTSVIEW")
        return competition, competitors
    finally:
        conn.close()


def get_table(conn, table):
    """ Return `table` from `conn` and return it as named tuple. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s" % table)
    data = cur.fetchall()
    desc = [description[0] for description in cur.description]
    cur.close()
    table_class = namedtuple(table, desc)
    return [table_class(*row) for row in data]
