from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView

from .models import Recode


class RecodeCreateView(CreateView):
    model = Recode

    fields = ('date', 'category', 'name', 'point')

    success_url = reverse_lazy('history:recode_list')

    def form_valid(self, form):
        executer = self.request.user
        form.instance.executer = executer
        return super().form_valid(form)


class RecodeDetailView(DetailView):
    model = Recode


class RecodeDeleteView(DeleteView):
    model = Recode

    success_url = reverse_lazy('history:recode_list')


class RecodeListView(ListView):
    model = Recode

    def get_queryset(self):
        return Recode.objects.filter(executer__in=self.request.user.group.users.all())
