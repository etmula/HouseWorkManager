from django.urls import path

from . import views

app_name = 'exec'
urlpatterns = [
    path('', views.index, name='index'),
]
