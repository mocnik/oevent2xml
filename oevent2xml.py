""" OEVENT 2 XML """

from collections import defaultdict
from datetime import datetime, timedelta

import pyxb.utils.domutils

import db
from iof import ResultStatus, ResultList, PersonResult, Person, PersonName, Namespace, \
    PersonRaceResult, Organisation, ClassResult, Class, STD_ANON, DateAndOptionalTime, \
    Event, Id

pyxb.utils.domutils.BindingDOMSupport.SetDefaultNamespace(Namespace)

STATUS_CODES = {
    0: ResultStatus.Active,
    1: ResultStatus.OK,
    2: ResultStatus.Disqualified,
    3: ResultStatus.DidNotFinish,
    4: ResultStatus.DidNotStart,
    5: ResultStatus.MissingPunch
}

CAT = {
    "M21E": "Men",
    "W21E": "Women"
}

def to_person_result(competitor, start_time, winning_time=None):
    """
    Args:
        competitor: competitor data from OEVENT db
        start_time: competition start time
    Returns:
        iof.PersonResult
    """
    start_tt = competitor.STARTTIME1 / 100 if competitor.STARTTIME1 else 0
    start = start_time + timedelta(seconds=start_tt)

    x_result = PersonResult()
    x_result.Person = Person.Factory(Name=PersonName.Factory(
        Given=competitor.FIRSTNAME, Family=competitor.LASTNAME))
    if competitor.WREID:
        iof_id = Id(int(competitor.WREID), type="IOF")
        x_result.Person.Id.append(iof_id)
    if competitor.CLUBLONGNAME:
        x_result.Organisation = Organisation.Factory(
            Name=competitor.CLUBLONGNAME)

    x_person_result = PersonRaceResult()
    x_person_result.Status = STATUS_CODES[competitor.FINISHTYPE1]
    x_person_result.StartTime = start.isoformat() + "+02:00"
    if competitor.COMPETITIONTIME1:
        x_person_result.Time = competitor.COMPETITIONTIME1 / 100
        if competitor.FINISHTYPE1 == 1:
            x_person_result.TimeBehind = (competitor.COMPETITIONTIME1 - winning_time) / 100

    x_result.Result.append(x_person_result)
    return x_result


def to_class_result(category, start_time):
    """
    Args:
        competitor: competitors for category from OEVENT db
        start_time: competition start time
    Returns:
        iof.ClassResult
    """
    x_class_result = ClassResult()
    x_class_result.Class = Class.Factory(
        Name=CAT[category[0].CATEGORYNAME], ShortName=CAT[category[0].CATEGORYNAME])
    winning_time = min(competitor.COMPETITIONTIME1
                       for competitor in category if competitor.FINISHTYPE1 == 1)

    for competitor in category:
        x_class_result.PersonResult.append(
            to_person_result(competitor, start_time, winning_time=winning_time))
    return x_class_result


def to_result_list(competition, categories):
    """
    Args:
        competition: competiton data from OEVENT db
        categories: competitors data from OEVENT db
    Returns:
        iof.ResultList
    """
    start_time = competition.DATE1 + timedelta(seconds=competition.FIRSTSTART1)
    x_start_time = DateAndOptionalTime.Factory(
        Date=start_time.date().isoformat(), Time=start_time.time().isoformat() + "+02:00")
    x_event = Event.Factory(Name=competition.COMPETITIONNAME, StartTime=x_start_time)

    x_result_list = ResultList()
    x_result_list.iofVersion = "3.0"
    x_result_list.Event = x_event
    x_result_list.createTime = datetime.now().isoformat() + "+02:00"
    x_result_list.creator = "OEVENT2XML v0.1"
    x_result_list.status = STD_ANON.Complete

    for _, category in categories.items():
        x_result_list.ClassResult.append(to_class_result(category, start_time))

    return x_result_list

def to_xml(connection_string):
    """
    Connects to the db, retrieves competition data and generates IOF v3 ResultList xml

    Returns:
        str: results in IOF v3 xml format
    """
    competition, competitors = db.get_data(connection_string)
    competition = competition[0]

    categories = defaultdict(list)

    for competitor in competitors:
        if (not competitor.ISVACANT) and competitor.ISRUNNING1 and \
           competitor.CATEGORYNAME in ["M21E", "W21E"] and competitor.WREID:
            categories[competitor.CATEGORYID].append(competitor)

    x_result_list = to_result_list(competition, categories)

    return x_result_list.toxml("utf-8")

if __name__ == "__main__":
    with open("r.xml", "wb") as f:
        f.write(to_xml("192.168.1.5:C:\\Users\\smocnik\\AppData\\Roaming\\OEvent\\Data\\Competition10.gdb"))
