import json

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, \
    DeleteView, ListView, UpdateView, TemplateView
from django import forms
from django.http.response import JsonResponse

from .models import Composite, Work, WorkExectedRecode
from stats.Charts import ExecutionRatePieChart, CategoryRatePieChart,\
    WorkPointShiftLineChart, NumberOfExecutionsBarChart


class CompositeListView(TemplateView):
    template_name = 'work/composite_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        composite_id = int(kwargs['pk'])
        if composite_id:
            parent = Composite.objects.get(
                group=self.request.user.group,
                id=composite_id
            )
        else:
            parent = None
        composites = Composite.objects.filter(
            group=self.request.user.group,
            parent=parent
        )
        works = Work.objects.filter(
            group=self.request.user.group,
            parent=parent
        )

        context['composite_list'] = composites.all()
        context['work_list'] = works.all()
        context['parent'] = parent
        return context


class CompositeCreateView(CreateView):
    model = Composite

    fields = ('parent', 'name',)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['parent'] = forms.ModelChoiceField(
            queryset=Composite.objects.filter(
                group=self.request.user.group
            ),
            required=False
        )
        return form

    def get_initial(self):
        initial = super().get_initial()
        composite_id = int(self.kwargs['pk'])
        if composite_id:
            initial["parent"] = Composite.objects.get(
                group=self.request.user.group,
                id=composite_id
            )
        return initial

    def form_valid(self, form):
        form.instance.group_id = self.request.user.group.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'work:composite_list',
            kwargs=dict(pk=self.get_form(self.form_class).instance.pk)
        )


class CompositeDeleteView(DeleteView):
    model = Composite

    def get_success_url(self):
        if self.object.parent:
            success_url = reverse_lazy('work:composite_detail', self.object.parent.id)
        else:
            success_url = reverse_lazy('work:composite_list')
        return success_url


class CompositeUpdateView(UpdateView):
    model = Composite

    fields = ('parent', 'name',)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['parent'] = forms.ModelChoiceField(
            queryset=Composite.objects.filter(
                group=self.request.user.group
            ),
            required=False
        )
        return form

    def get_initial(self):
        initial = super().get_initial()
        composite_id = int(self.kwargs['pk'])
        if composite_id:
            composite = Composite.objects.get(
                group=self.request.user.group,
                id=composite_id
            )
            initial["parent"] = composite.parent
        return initial

    def form_valid(self, form):
        form.instance.group_id = self.request.user.group.id
        return super().form_valid(form)


class WorkCreateView(CreateView):
    model = Work

    fields = ('parent', 'name', 'point', 'description', 'alert')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['parent'] = forms.ModelChoiceField(
            queryset=Composite.objects.filter(
                group=self.request.user.group
            ),
            required=False
        )
        return form

    def get_initial(self):
        initial = super().get_initial()
        composite_id = int(self.kwargs['pk'])
        if composite_id:
            initial["parent"] = Composite.objects.get(
                group=self.request.user.group,
                id=composite_id
            )
        return initial

    def form_valid(self, form):
        form.instance.group_id = self.request.user.group.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'work:work_detail',
            kwargs=dict(pk=self.get_form(self.form_class).instance.pk)
        )


class WorkUpdateView(UpdateView):
    model = Work

    fields = ('parent', 'name', 'point', 'description', 'alert')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['parent'] = forms.ModelChoiceField(
            queryset=Composite.objects.filter(
                group=self.request.user.group
            ),
            required=False
        )
        return form

    def form_valid(self, form):
        form.instance.group_id = self.request.user.group.id
        return super().form_valid(form)


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

    def get_success_url(self):
        if self.object.parent:
            success_url = reverse_lazy('work:composite_detail', self.object.parent.id)
        else:
            success_url = reverse_lazy('work:composite_list')
        return success_url


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
