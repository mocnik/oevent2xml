import db
import iof

from datetime import datetime, timedelta

competition, competitors = db.get_data()
competition = competition[0]
competitor = competitors[0]

start_time = competition.DATE1 + timedelta(seconds=competition.FIRSTSTART1)

x_start_time = iof.DateAndOptionalTime.Factory(Date=start_time.date().isoformat(), Time=start_time.time().isoformat() + "+02:00")
x_event = iof.Event.Factory(Name=competition.COMPETITIONNAME, StartTime=x_start_time)

x_result_list = iof.ResultList()
x_result_list.iofVersion = "3.0"
x_result_list.Event = x_event
x_result_list.createTime = datetime.now().isoformat() + "+02:00"
x_result_list.creator = "OEVENT2XML v0.1"
x_result_list.status = iof.STD_ANON.Snapshot

x_class_result = iof.ClassResult()
x_class_result.Class = iof.Class.Factory(Name=competitor.CATEGORYNAME, ShortName=competitor.CATEGORYNAME)

x_result = iof.PersonResult()
x_result.Person =  iof.Person.Factory(Name=iof.PersonName.Factory(Given=competitor.FIRSTNAME, Family=competitor.LASTNAME))
x_result.Organisation = iof.Organisation.Factory(Name=competitor.CLUBLONGNAME)

x_person_result = iof.PersonRaceResult()
x_person_result.Status = iof.ResultStatus.OK
x_person_result.StartTime = "2016-05-18T12:00:00Z"
x_person_result.FinishTime = "2016-05-18T12:28:15Z"
x_person_result.Time = 1695
x_person_result.TimeBehind = 0
x_person_result.Position = 1

x_result.Result.append(x_person_result)

x_class_result.PersonResult.append(x_result)

x_result_list.ClassResult.append(x_class_result)

print(x_result_list.toxml("UTF-8"))
