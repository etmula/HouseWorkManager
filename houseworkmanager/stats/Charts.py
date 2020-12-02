from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime, timedelta, date
import itertools

from work.models import Work, WorkExectedRecode


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
    '''ある仕事の、ユーザー毎の実行数円グラフ
    '''

    @classmethod
    def title(cls):
        return 'ExecutionRatePieChart'

    @classmethod
    def js_path(cls):
        return 'stats/js/pie_chart.js'

    def build_table(self, work, startdate=None, enddate=None):
        users = self.group.users
        table = [['username', 'ExecutionRate'], ]
        for user in users.all():
            recodes = WorkExectedRecode.objects.filter(
                group=self.group,
                work=work,
                executers=user
            )
            if startdate:
                recodes = recodes.filter(exected_date__gte=startdate)
            if enddate:
                recodes = recodes.filter(exected_date__lte=enddate)
            row = [user.username, len(recodes)]
            table.append(row)
        self.table = table


class NumberOfExecutionsBarChart(Chart):
    '''ユーザー:仕事 の実行数棒グラフ
    '''

    @classmethod
    def title(cls):
        return 'NumberOfExecutionsBarChart'

    @classmethod
    def js_path(cls):
        return 'stats/js/bar_chart.js'

    def build_table(self, startdate=None, enddate=None):
        table = [['work_name', ] + [user.username for user in self.group.users.all()],]
        for work in self.group.works.all():
            row = [work.name, ]
            for user in self.group.users.all():
                recodes = WorkExectedRecode.objects.filter(
                    group=self.group,
                    work=work,
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
    '''
    '''

    @classmethod
    def title(cls):
        return 'ScoreIncreaseLineChart'

    @classmethod
    def js_path(cls):
        return 'stats/js/line_chart.js'

    def build_table(self, startdate, enddate):
        table = [
            ['date', ] + [user.username for user in self.group.users.all()] +
            [
                ['date', ]+[
                    user.calc_point(
                        startdate=startdate,
                        enddate=startdate+timedelta(days=i)
                    )
                    for user in self.group.users.all()
                ]
                for i in range((enddate - startdate).days + 1)
            ]
        ]
        self.table = table


class CategoryRatePieChart(Chart):

    @classmethod
    def title(cls):
        return '各Categoryが実行された回数の割合'

    @classmethod
    def js_path(cls):
        return 'stats/js/pie_chart.js'

    def build_table(self, startdate=None, enddate=None):
        '''各Categoryが実行された回数の割合
        '''
        table = [['category', 'ExecutionRate'], ]
        for category in self.group.categorys.all():
            recodes = self.group.workexectedrecodes.filter(
                work__in=category.works.all()
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
        table = [
            ['date', 'point'] +
            [
                [recode.updated_at, recode.point]
                for recode in work.workupdatedrecodes
            ]
        ]
        self.table = table
