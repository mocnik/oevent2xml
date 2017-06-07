import firebirdsql

from collections import namedtuple

USER = 'SYSDBA'
PASSWORD = 'masterkey'
CONNECTION_STRING = 'localhost:C:\\Users\\ASUS-Rok\\AppData\\Roaming\\OEvent\\Data\\COMPETITION11.GDB'

SELECT_COMPETITORS = 'SELECT * FROM OEVLISTSVIEW'
SELECT_COMPETITION_DATA = 'SELECT * FROM OEVCOMPETITION'

# cur.describe
# (name, type_code, display_size, internal_size, precision, scale, null_ok)

def get_data():
    conn = firebirdsql.connect(dsn=CONNECTION_STRING, user=USER, password=PASSWORD)
    cur = conn.cursor()
    cur.execute(SELECT_COMPETITORS)
    data = cur.fetchall()
    description = cur.description
    cur.close()
    conn.close()
    return data, description

def get_competitors():
    competitors, desc = get_data()
    description = [d[0] for d in desc]
    competitor_class = namedtuple('Competitor', description)
    return [competitor_class(*competitor) for competitor in competitors]
