from django.urls import path

from . import views

app_name = 'exec'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('exec', views.ExecView.as_view(), name='exec'),
]
