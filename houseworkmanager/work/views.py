from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.forms import inlineformset_factory
from django import forms

from .models import Work, Category
from accounts.models import Group


class WorkCreateView(CreateView):
    model = Work

    fields = ('category', 'name', 'point', 'description', 'alert')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        queryset = Category.objects.filter(group=user.group)
        form.fields['category'] = forms.ModelChoiceField(queryset=queryset)
        return form

    def get_form_kwargs(self, *args, **kwargs):
        # print(super(CreateView, self).get_form_kwargs(*args, **kwargs))
        kwargs = super(CreateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class WorkDetailView(DetailView):
    model = Work


class WorkDeleteView(DeleteView):
    model = Work

    success_url = reverse_lazy('work:work_list')


class WorkListView(ListView):
    model = Work

    def get_queryset(self):   
        return Work.objects.filter(category__in=self.request.user.group.categorys.all())


class WorkUpdateView(UpdateView):
    model = Work

    fields = ('category', 'name', 'point', 'description', 'alert')


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
        print(self.kwargs['pk'])
        category = Category.objects.get(pk=self.kwargs['pk'])
        print(category)
        context['work_list'] = category.works.all()
        print(context['work_list'])
        return context


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        # Category.objects.filter(group=)
        return super().get_queryset()


class CategoryUpdateView(UpdateView):
    model = Category

    fields = ('name',)