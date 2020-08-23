import calendar
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView, TemplateView
from django.utils import timezone

from .models import Recode
from stats.table_generator import score_user_line
from stats.Charts import NumberOfExecutionsBarChart


class RecodeCreateView(CreateView):
    model = Recode

    fields = ('exected_date', 'executers', 'workcommit')

    success_url = reverse_lazy('history:recode_list')

    def form_valid(self, form):
        group = self.request.user.group
        form.instance.group = group
        return super().form_valid(form)


class RecodeDetailView(DetailView):
    model = Recode


class RecodeDeleteView(DeleteView):
    model = Recode

    success_url = reverse_lazy('history:recode_list')


class RecodeListView(ListView):
    model = Recode

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        chart = NumberOfExecutionsBarChart(self.request.user.group)
        chart.build_table()
        context['chart'] = chart
        return context

    def get_queryset(self):
        recodes = Recode.objects.filter(
            group=self.request.user.group
        ).order_by('created_at')
        return recodes.all()


class RecodePointTableMonthlyView(TemplateView):
    template_name = 'history/point_table_monthly.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        point_table_dict = {
            'title': 'PointTable',
            'table': self.request.user.group.build_point_table_monthly(year, month)
        }
        context['point_table_dict'] = point_table_dict
        return context


class RecodeCountTableMonthlyView(TemplateView):
    template_name = 'history/count_table_monthly.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        count_table_dict = {
            'title': 'CountTable',
            'table': self.request.user.group.build_count_table_monthly(year, month)
        }
        context['count_table_dict'] = count_table_dict
        return context


class RecodeListMonthlyView(ListView):
    model = Recode
    template_name = 'history/recode_list_monthly.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        first_date = date(year, month, 1)
        last_date = date(year, month, calendar.monthrange(year, month)[1])
        context['first_date'] = first_date
        context['next_date'] = first_date + relativedelta(months=1)
        context['before_date'] = first_date - relativedelta(months=1)
        chart = NumberOfExecutionsBarChart(self.request.user.group)
        chart.build_table(startdate=first_date, enddate=last_date)
        context['chart'] = chart
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(exected_date__year=self.kwargs.get('year'), exected_date__month=self.kwargs.get('month'))
        return query_set

    
