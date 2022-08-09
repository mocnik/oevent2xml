""" OEVENT 2 XML """

from collections import defaultdict
from datetime import datetime, timedelta

import pyxb.utils.domutils

import db
from iof import ResultStatus, ResultList, PersonResult, Person, PersonName, Namespace, \
    PersonRaceResult, Organisation, ClassResult, Class, STD_ANON, DateAndOptionalTime, Event

pyxb.utils.domutils.BindingDOMSupport.SetDefaultNamespace(Namespace)

STATUS_CODES = {
    0: ResultStatus.Active,
    1: ResultStatus.OK,
    2: ResultStatus.Disqualified,
    3: ResultStatus.DidNotFinish,
    4: ResultStatus.DidNotStart,
    5: ResultStatus.MissingPunch
}


def to_person_result(competitor, start_time, stage = 1):
    """
    Args:
        competitor: competitor data from OEVENT db
        start_time: competition start time
    Returns:
        iof.PersonResult
    """
    try:
        if stage == 1:
            start = start_time + timedelta(seconds=competitor.STARTTIME1 / 100)
        elif stage == 2:
            start = start_time + timedelta(seconds=competitor.STARTTIME2 / 100)
        elif stage == 3:
            start = start_time + timedelta(seconds=competitor.STARTTIME3 / 100)
        elif stage == 4:
            start = start_time + timedelta(seconds=competitor.STARTTIME4 / 100)
        elif stage == 5:
            start = start_time + timedelta(seconds=competitor.STARTTIME5 / 100)
    except:
        start = start_time

    x_result = PersonResult()
    x_result.Person = Person.Factory(Name=PersonName.Factory(
        Given=competitor.FIRSTNAME, Family=competitor.LASTNAME))
    if competitor.CLUBLONGNAME:
        x_result.Organisation = Organisation.Factory(
            Name=competitor.CLUBLONGNAME)

    x_person_result = PersonRaceResult()

    if stage == 1:
        x_person_result.Status = STATUS_CODES[competitor.FINISHTYPE1]
        x_person_result.StartTime = start.isoformat() + "+02:00"
        if competitor.COMPETITIONTIME1:
            x_person_result.Time = competitor.COMPETITIONTIME1 / 100
    elif stage == 2:
        x_person_result.Status = STATUS_CODES[competitor.FINISHTYPE2]
        x_person_result.StartTime = start.isoformat() + "+02:00"
        if competitor.COMPETITIONTIME2:
            x_person_result.Time = competitor.COMPETITIONTIME2 / 100
    elif stage == 3:
        x_person_result.Status = STATUS_CODES[competitor.FINISHTYPE3]
        x_person_result.StartTime = start.isoformat() + "+02:00"
        if competitor.COMPETITIONTIME3:
            x_person_result.Time = competitor.COMPETITIONTIME3 / 100
    elif stage == 4:
        x_person_result.Status = STATUS_CODES[competitor.FINISHTYPE4]
        x_person_result.StartTime = start.isoformat() + "+02:00"
        if competitor.COMPETITIONTIME4:
            x_person_result.Time = competitor.COMPETITIONTIME4 / 100
    elif stage == 5:
        x_person_result.Status = STATUS_CODES[competitor.FINISHTYPE5]
        x_person_result.StartTime = start.isoformat() + "+02:00"
        if competitor.COMPETITIONTIME5:
            x_person_result.Time = competitor.COMPETITIONTIME5 / 100


    x_result.Result.append(x_person_result)
    return x_result


def to_class_result(category, start_time, stage = 1):
    """
    Args:
        competitor: competitors for category from OEVENT db
        start_time: competition start time
    Returns:
        iof.ClassResult
    """
    x_class_result = ClassResult()
    x_class_result.Class = Class.Factory(
        Name=category[0].CATEGORYNAME, ShortName=category[0].CATEGORYNAME)

    for competitor in category:
        x_class_result.PersonResult.append(to_person_result(competitor, start_time, stage))
    return x_class_result


def to_result_list(competition, categories, stage = 1):
    """
    Args:
        competition: competiton data from OEVENT db
        categories: competitors data from OEVENT db
    Returns:
        iof.ResultList
    """
    if stage == 1:
        start_time = competition.DATE1 + timedelta(seconds=competition.FIRSTSTART1)
    elif stage == 2:
        start_time = competition.DATE2 + timedelta(seconds=competition.FIRSTSTART2)
    elif stage == 3:
        start_time = competition.DATE3 + timedelta(seconds=competition.FIRSTSTART3)
    elif stage == 4:
        start_time = competition.DATE4 + timedelta(seconds=competition.FIRSTSTART4)
    elif stage == 5:
        start_time = competition.DATE5 + timedelta(seconds=competition.FIRSTSTART5)

    x_start_time = DateAndOptionalTime.Factory(
        Date=start_time.date().isoformat(), Time=start_time.time().isoformat() + "+02:00")
    x_event = Event.Factory(Name=competition.COMPETITIONNAME, StartTime=x_start_time)

    x_result_list = ResultList()
    x_result_list.iofVersion = "3.0"
    x_result_list.Event = x_event
    x_result_list.createTime = datetime.now().isoformat() + "+02:00"
    x_result_list.creator = "OEVENT2XML v0.1"
    x_result_list.status = STD_ANON.Snapshot

    for _, category in categories.items():
        x_result_list.ClassResult.append(to_class_result(category, start_time, stage))

    return x_result_list

def to_xml(connection_string, stage = 1):
    """
    Connects to the db, retrieves competition data and generates IOF v3 ResultList xml

    Returns:
        str: results in IOF v3 xml format
    """
    competition, competitors = db.get_data(connection_string)
    competition = competition[0]

    categories = defaultdict(list)

    for competitor in competitors:
        if stage == 1:
            if (not competitor.ISVACANT) and competitor.ISRUNNING1:
                categories[competitor.CATEGORYID].append(competitor)
        elif stage == 2:
            if (not competitor.ISVACANT) and competitor.ISRUNNING2:
                categories[competitor.CATEGORYID].append(competitor)
        elif stage == 3:
            if (not competitor.ISVACANT) and competitor.ISRUNNING3:
                categories[competitor.CATEGORYID].append(competitor)
        elif stage == 4:
            if (not competitor.ISVACANT) and competitor.ISRUNNING4:
                categories[competitor.CATEGORYID].append(competitor)
        elif stage == 5:
            if (not competitor.ISVACANT) and competitor.ISRUNNING5:
                categories[competitor.CATEGORYID].append(competitor)

    x_result_list = to_result_list(competition, categories, stage)

    return x_result_list.toxml("utf-8")

if __name__ == "__main__":
    with open("r.xml", "wb") as f:
        f.write(to_xml("192.168.1.5:C:\\Users\\smocnik\\AppData\\Roaming\\OEvent\\Data\\Competition10.gdb"))
