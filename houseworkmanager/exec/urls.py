from django.urls import path

from . import views

app_name = 'exec'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('exec', views.ExecView.as_view(), name='exec'),
    path('history', views.HistoryView.as_view(), name='history'),
    path('work', views.WorkView.as_view(), name='work'),
    path('category', views.CategoryView.as_view(), name='category'),
]
