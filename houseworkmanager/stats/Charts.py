from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime, timedelta, date

from work.models import WorkCommit


class Chart(metaclass=ABCMeta):
    
    def __init__(self, group):
        self.group = group
        self.table = None

    @classmethod
    @abstractmethod
    def title(cls):
        pass

    @classmethod
    @abstractmethod
    def js_path(cls):
        pass

    @abstractmethod
    def build_table(self, startdate=None, enddate=None):
        pass


class ExecutionRatePieChart(Chart):

    @classmethod
    def title(cls):
        return 'ExecutionRatePieChart'

    @classmethod
    def js_path(cls):
        return 'stats/js/pie_chart.js'

    def build_table(self, work, startdate=None, enddate=None):
        users = self.group.users
        table = [['username', 'ExecutionRate'],]
        for user in users.all():
            row = [user.username, user.calc_work_count(work=work, startdate=startdate, enddate=enddate)]
            table.append(row)
        self.table = table
    

class NumberOfExecutionsBarChart(Chart):

    @classmethod
    def title(cls):
        return 'NumberOfExecutionsBarChart'
    
    @classmethod
    def js_path(cls):
        return 'stats/js/bar_chart.js'

    def build_table(self, startdate=None, enddate=None):
        users = self.group.users
        categorys = self.group.categorys
        works = category.works
        table = [['work_name',] + [user.username for user in users.all()],]
        for work in works.all():
            row = [work.head.name,] + [user.calc_work_count(work=work, startdate=startdate, enddate=enddate) for user in users.all()]
            table.append(row)
        self.table = table


class ScoreIncreaseLineChart(Chart):

    @classmethod
    def title(cls):
        return 'ScoreIncreaseLineChart'
    
    @classmethod
    def js_path(cls):
        return 'stats/js/line_chart.js'

    def build_table(self, startdate=None, enddate=None):
        users = self.group.users
        table = [['date',] + [user.username for user in users.all()],]
        for i in range((enddate - startdate).days + 1):
            date = startdate + timedelta(days=i)
            row = [date.day,]
            for user in users.all():
                row.append(user.calc_work_point(work=work, startdate=startdate, enddate=date))
            table.append(row)
        self.table = table
