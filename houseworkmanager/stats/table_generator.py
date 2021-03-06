import calendar
from datetime import datetime

from django.shortcuts import render

from work.models import WorkExectedRecode


def score_user_line(users, year, month):
    data = [['day',],]
    data[0].extend([user.username for user in users])
    startdate = datetime(year, month, 1)
    for day in range(calendar.monthrange(year, month)[1]):
        day += 1
        date = datetime(year, month, day)
        row = [date.day,]
        for user in users:
            row.append(user.calc_point(startdate=startdate, enddate=date))
        data.append(row)
    return data


def work_exected_column(group, year, month):
    data = [['work',],]
    startdate = datetime(year, month, 1)
    enddate = datetime(year, month, calendar.monthrange(year, month)[1])
    recodes = Recode.objects.filter(group=group, date__range=[startdate, enddate])
    users = []
    for recode in recodes:
        if not recode.executer in users:
            users.append(recode.executer)
    
    recode_dict = {}
    for recode in recodes:
        if not recode.name in recode_dict:
            recode_dict[recode.name] = {user:0 for user in users}
        recode_dict[recode.name][recode.executer] += 1

    data[0].extend([user.username for user in users])
    for workname in recode_dict.keys():
        row = [workname,]
        row.extend([recode_dict[workname][user] for user in users])
        data.append(row)
    return data