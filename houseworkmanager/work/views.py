from urllib.parse import urlencode

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.forms import inlineformset_factory
from django import forms

from .models import Work, Category, WorkCommit
from accounts.models import Group
from history.models import Recode
from stats.Charts import ExecutionRatePieChart, CategoryRatePieChart, WorkPointShiftLineChart


class WorkCommitCreateView(CreateView):
    model = WorkCommit

    fields = ('name', 'description', 'point')

    def get_initial(self):
        initial = super().get_initial()
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        if work.head:
            initial['name'] = work.head.name
            initial['description'] = work.head.description
            initial['point'] = work.head.point
        return initial

    def form_valid(self, form):
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        form.instance.work_id = work.id
        work.head = form.instance
        return super().form_valid(form)
    
    def get_success_url(self):
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        work.head = self.object
        work.save()
        return reverse('work:work_detail', kwargs={'pk': work.pk})


class WorkCommitListView(ListView):
    model = WorkCommit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        chart = WorkPointShiftLineChart(self.request.user.group)
        chart.build_table(work=work)
        context["chart"] = chart
        context["work"] = work
        return context
    
    def get_queryset(self):
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        return WorkCommit.objects.filter(work=work)


class WorkCommitDetailView(DetailView):
    model = WorkCommit


class WorkCreateView(CreateView):
    model = Work

    fields = ('category', 'alert')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        queryset = Category.objects.filter(group=user.group)
        form.fields['category'] = forms.ModelChoiceField(queryset=queryset)
        return form

    def get_success_url(self):
        return reverse('work:workcommit_create', kwargs=dict(pk=self.get_form(self.form_class).instance.pk))


class WorkDetailView(DetailView):
    model = Work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chart = ExecutionRatePieChart(self.request.user.group)
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        chart.build_table(work=work)
        context["chart"] = chart
        return context
    


class WorkDeleteView(DeleteView):
    model = Work

    success_url = reverse_lazy('work:work_list')


class WorkExectedRecodeListView(ListView):
    model = WorkExectedRecode

    def get_queryset(self):   
        workexectedrecodes = WorkExectedRecode.objects.filter(
            group=self.request.user.group
        )
        if 'pk' in self.kwargs:
            work_id = int(self.kwargs['pk'])
            workexectedrecodes = WorkExectedRecode.objects.filter(
                work=Work.objects.get(id=work_id)
            )
        return workexectedrecodes.order_by('-created_at').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chart = NumberOfExecutionsBarChart(self.request.user.group)
        chart.build_table()
        context['chart'] = chart
        return context


class WorkExectedRecodeCreateView(CreateView):
    model = WorkExectedRecode

    fields = ('exected_date', 'executers', 'work', 'name', 'point',)

    success_url = reverse_lazy('work:WorkExectedRecode_list')

    def form_valid(self, form):
        group = self.request.user.group
        form.instance.group = group
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        executers = [int(user_id) for user_id in data["executers"]]
        work = Work.objects.get(
            group=request.user.group,
            id=int(data["work"])
        )
        date = data["date"]
        workexectedrecode = WorkExectedRecode.objects.create(
            exected_date=date,
            work=work,
            group=request.user.group,
            name=work.name,
            point=work.point
        )
        workexectedrecode.executers.set(executers)
        return JsonResponse({})

    
class WorkExectedRecodeDetailView(DetailView):
    model = WorkExectedRecode


class WorkExectedRecodeDeleteView(DeleteView):
    model = WorkExectedRecode

    success_url = reverse_lazy('work:WorkExectedRecode_list')
