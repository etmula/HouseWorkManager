from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime, timedelta, date
import itertools

from work.models import WorkCommit, Work, Category
from history.models import Recode


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
            workcommits = WorkCommit.objects.filter(
                work=work
            )
            recodes = Recode.objects.filter(
                group=self.group,
                workcommit__in=workcommits
            )
            if startdate:
                recodes = recodes.filter(exected_date__gte=startdate)
            if enddate:
                recodes = recodes.filter(exected_date__lte=enddate)
            row = [user.username, len(recodes)]
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
        works = []
        for category in self.group.categorys.all():
            if category.works.all():
                works.extend(category.works.all())
        table = [['work_name',] + [user.username for user in users.all()],]
        for work in works:
            row = [work.head.name,]
            for user in users.all():
                workcommits = WorkCommit.objects.filter(work=work)
                recodes = Recode.objects.filter(
                    group=self.group,
                    workcommit__in=workcommits,
                    executers=user
                )
                if startdate:
                    recodes = recodes.filter(exected_date__gte=startdate)
                if enddate:
                    recodes = recodes.filter(exected_date__lte=enddate)
                row.append(len(recodes))
            table.append(row)
        self.table = table


class ScoreIncreaseLineChart(Chart):

    @classmethod
    def title(cls):
        return 'ScoreIncreaseLineChart'
    
    @classmethod
    def js_path(cls):
        return 'stats/js/line_chart.js'

    def build_table(self, startdate, enddate):
        users = self.group.users
        table = [['date',] + [user.username for user in users.all()],]
        for i in range((enddate - startdate).days + 1):
            date = startdate + timedelta(days=i)
            row = [date.day,]
            for user in users.all():
                row.append(user.calc_point(startdate=startdate, enddate=date))
            table.append(row)
        self.table = table


class CategoryRatePieChart(Chart):

    @classmethod
    def title(cls):
        return '各Categoryが実行された回数の割合'

    @classmethod
    def js_path(cls):
        return 'stats/js/pie_chart.js'

    def build_table(self, startdate=None, enddate=None):
        users = self.group.users
        table = [['category', 'ExecutionRate'],]
        for category in self.group.categorys.all():
            works = Work.objects.filter(category=category)
            workcommits = []
            for work in works:
                workcommits.extend(work.commits.all())
            recodes = Recode.objects.filter(
                group=self.group,
                workcommit__in=workcommits
            )
            if startdate:
                recodes = recodes.filter(exected_date__gte=startdate)
            if enddate:
                recodes = recodes.filter(exected_date__lte=enddate)
            row = [category.name, len(recodes)]
            table.append(row)
        self.table = table


class WorkPointShiftLineChart(Chart):

    @classmethod
    def title(cls):
        return 'WorkPointShiftLineChart'
    
    @classmethod
    def js_path(cls):
        return 'stats/js/line_chart.js'

    def build_table(self, work):
        workcommits = work.commits.order_by('created_at')
        table = [['date', 'point'],]
        for workcommit in workcommits.all():
            row = [date(workcommit.created_at.year, workcommit.created_at.month, workcommit.created_at.day), workcommit.point]
            table.append(row)
        self.table = table
