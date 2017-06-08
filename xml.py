import db
import iof

from datetime import datetime, timedelta

competition, competitors = db.get_data()
competition = competition[0]

start_time = competition.DATE1 + timedelta(seconds=competition.FIRSTSTART1)

x_start_time = iof.DateAndOptionalTime.Factory(Date=start_time.date().isoformat(), Time=start_time.time().isoformat() + "+02:00")
x_event = iof.Event.Factory(Name=competition.COMPETITIONNAME, StartTime=x_start_time)

x_result_list = iof.ResultList()
x_result_list.iofVersion = "3.0"
x_result_list.Event = x_event
x_result_list.createTime = datetime.now().isoformat() + "+02:00"
x_result_list.creator = "OEVENT2XML v0.1"
print(x_result_list.toxml("UTF-8"))
