import json

from django.shortcuts import reverse, HttpResponse
from django.views.generic import TemplateView, ListView
from django.utils.functional import cached_property

from history.models import Recode
from history.views import RecodeListView
from work.views import WorkListView, CategoryListView


class ExecView(TemplateView):
    template_name = 'exec/exec.html'
    
    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('utf-8')
        json_data = json.loads(json_str)
        if 'works' in json_data:
            executer = request.user
            recodes = []
            for work in json_data['works']:
                recode = Recode(
                    executer=executer,
                    date=work['date'],
                    category=work['category'],
                    name=work['name'],
                    point=int(work['point'])
                )
                recodes.append(recode)
            Recode.objects.bulk_create(recodes)
        return HttpResponse(reverse('exec:home'))

    @cached_property
    def group(self):
        return self.request.user.group


class HomeView(TemplateView):
    template_name = 'exec/home.html'

    @cached_property
    def group(self):
        return self.request.user.group


class HistoryView(RecodeListView):
    template_name = 'exec/history.html'


class WorkView(WorkListView):
    template_name = 'exec/work.html'

class CategoryView(CategoryListView):
    template_name = 'exec/category.html'