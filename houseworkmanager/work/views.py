from urllib.parse import urlencode

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.forms import inlineformset_factory
from django import forms

from .models import Work, Category, WorkCommit
from accounts.models import Group
from history.models import Recode
from stats.Charts import ExecutionRatePieChart


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
        context["work"] = Work.objects.get(pk=self.kwargs.get('pk'))
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
        print(self.kwargs.get('pk'))
        work = Work.objects.get(pk=self.kwargs.get('pk'))
        print(work)
        chart.build_table(work=work)
        context["chart"] = chart
        return context
    


class WorkDeleteView(DeleteView):
    model = Work

    success_url = reverse_lazy('work:work_list')


class WorkListView(ListView):
    model = Work

    def get_queryset(self):   
        return Work.objects.filter(category__in=self.request.user.group.categorys.all())


class WorkUpdateView(UpdateView):
    model = Work

    fields = ('category', 'alert')


class CategoryCreateView(CreateView):
    model = Category

    fields = ('name',)

    success_url = reverse_lazy('work:category_list')

    def form_valid(self, form):
        group = self.request.user.group
        form.instance.group_id = group.id
        return super().form_valid(form)


class CategoryDetailView(DetailView):
    model = Category


class CategoryDeleteView(DeleteView):
    model = Category

    success_url = reverse_lazy('work:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['work_list'] = category.works.all()
        return context


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        # Category.objects.filter(group=)
        return super().get_queryset()


class CategoryUpdateView(UpdateView):
    model = Category

    fields = ('name',)