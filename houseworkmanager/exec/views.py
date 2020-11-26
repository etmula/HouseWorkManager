import calendar
import json
from datetime import date

from django.shortcuts import reverse, HttpResponse
from django.views.generic import TemplateView, ListView
from django.utils.functional import cached_property
from django.utils import timezone

from accounts.models import User
from history.models import Recode
from work.models import Work
from history.views import RecodeListView
from work.views import WorkListView, CategoryListView
from stats.table_generator import score_user_line, work_exected_column
from stats.Charts import ScoreIncreaseLineChart


class ExecView(TemplateView):
    template_name = 'exec/exec.html'
    
    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('utf-8')
        json_data = json.loads(json_str)
        if 'works' in json_data:
            for work in json_data['works']:
                workcommit = Work.objects.get(pk=work['pk']).head
                executers = User.objects.filter(pk__in=list(work['executers'])).all()
                recode = Recode.objects.create(
                    exected_date=work['exected_date'],
                    workcommit=workcommit,
                    group=request.user.group,
                )
                recode.executers.set(executers.all())
        return HttpResponse(reverse('exec:home'))

    @cached_property
    def group(self):
        return self.request.user.group


class HomeView(TemplateView):
    template_name = 'exec/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['current_date'] = now
        chart = ScoreIncreaseLineChart(self.request.user.group)
        now = timezone.now()
        startdate = date(year=now.year, month=now.month, day=1)
        enddate = date(year=now.year, month=now.month, day=calendar.monthrange(now.year, now.month)[1])
        chart.build_table(startdate=startdate, enddate=enddate)
        context['chart'] = chart
        return context

    @cached_property
    def group(self):
        return self.request.user.group
