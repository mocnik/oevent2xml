""" Module connecting to OEVENT Firebird SQL database and exporting competition data. """
from collections import namedtuple

import firebirdsql

USER = 'SYSDBA'
PASSWORD = 'masterkey'

SQL = """
select oevCompetitor.ID as CompetitorID, StartNumber, CategoryName, FirstName, LastName, oevCountry.LongName as CountryLongName, oevCountry.ShortName as CountryShortName, 
oevClub.LongName as ClubLongName,  oevClub.ShortName as ClubShortName, oevCategory.ID as CategoryID,
oevClub.ID as ClubID, IsVacant, wreID,
ChipNumber1, ChipNumber2, ChipNumber3, ChipNumber4, ChipNumber5, ChipNumber6, ChipNumber7, ChipNumber8, ChipNumber9, ChipNumber10,
StartTime1, StartTime2, StartTime3, StartTime4, StartTime5, StartTime6, StartTime7, StartTime8, StartTime9, StartTime10,
FinishTime1, FinishTime2, FinishTime3, FinishTime4, FinishTime5, FinishTime6, FinishTime7, FinishTime8, FinishTime9, FinishTime10,
FinishType1, FinishType2, FinishType3, FinishType4, FinishType5, FinishType6, FinishType7, FinishType8, FinishType9, FinishType10,
NotClassified1, NotClassified2, NotClassified3, NotClassified4, NotClassified5,
NotClassified6, NotClassified7, NotClassified8, NotClassified9, NotClassified10,
CompetitionTime1, CompetitionTime2, CompetitionTime3, CompetitionTime4, CompetitionTime5, 
CompetitionTime6, CompetitionTime7, CompetitionTime8, CompetitionTime9, CompetitionTime10, 
coalesce (oevCompetitor.COURSEID1, OEVCATEGORY.CourseID1) as CourseID1,
coalesce (oevCompetitor.COURSEID2, OEVCATEGORY.CourseID2) as CourseID2,
coalesce (oevCompetitor.COURSEID3, OEVCATEGORY.CourseID3) as CourseID3,
coalesce (oevCompetitor.COURSEID4, OEVCATEGORY.CourseID4) as CourseID4,
coalesce (oevCompetitor.COURSEID5, OEVCATEGORY.CourseID5) as CourseID5,
coalesce (oevCompetitor.COURSEID6, OEVCATEGORY.CourseID6) as CourseID6,
coalesce (oevCompetitor.COURSEID7, OEVCATEGORY.CourseID7) as CourseID7,
coalesce (oevCompetitor.COURSEID8, OEVCATEGORY.CourseID8) as CourseID8,
coalesce (oevCompetitor.COURSEID9, OEVCATEGORY.CourseID9) as CourseID9,
coalesce (oevCompetitor.COURSEID10, OEVCATEGORY.CourseID10) as CourseID10,
IsRunning1, IsRunning2, IsRunning3, IsRunning4, IsRunning5, IsRunning6, IsRunning7, IsRunning8, IsRunning9, IsRunning10, RESULTISREMOTE1,
  RESULTISREMOTE2,
  RESULTISREMOTE3,
  RESULTISREMOTE4,
  RESULTISREMOTE5,
  RESULTISREMOTE6,
  RESULTISREMOTE7,
  RESULTISREMOTE8,
  RESULTISREMOTE9,
  RESULTISREMOTE10
from oevCategory, oevCompetitor  left outer join
oevClub on ClubID = oevClub.ID
left outer join oevCountry on oevClub.CountryID = oevCountry.ID
where CategoryID = oevCategory.ID;
"""

def get_data(connection_string):
    """ Get competition data from firebird sql database at `connection_string`. """
    conn = firebirdsql.connect(dsn=connection_string, user=USER, password=PASSWORD)
    try:
        competition = get_table(conn, "SELECT * FROM OEVCOMPETITION")
        competitors = get_table(conn, SQL)
        return competition, competitors
    finally:
        conn.close()


def get_table(conn, sql):
    """ Return `table` from `conn` and return it as named tuple. """
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    desc = [description[0] for description in cur.description]
    cur.close()
    table_class = namedtuple('info', desc)
    return [table_class(*row) for row in data]
