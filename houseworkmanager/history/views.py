from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.utils import timezone

from .models import Recode
from stats.table_generator import score_user_line

def RecodeCancel(request):
    request.POST.get()
    return reverse_lazy('history:recode_list')


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['data'] = score_user_line(self.request.user.group.users.all(), now.year, now.month)
        return context

    def get_queryset(self):
        return Recode.objects.filter(executer__in=self.request.user.group.users.all())


class RecodeListMonthlyView(ListView):
    model = Recode

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = score_user_line(self.request.user.group.users.all(), self.kwargs.get('year'), self.kwargs.get('month'))
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set.filter(date__year=self.kwargs.get('year'), date__month=self.kwargs.get('month'))
        return query_set

    
