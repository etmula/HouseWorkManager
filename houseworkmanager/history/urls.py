from django.urls import path

from . import views

app_name = 'history'
urlpatterns = [
    path('recode/', views.RecodeListView.as_view(), name='recode_list'),
    path('recode/<int:pk>', views.RecodeDetailView.as_view(), name='recode_detail'),
    path('recode/create', views.RecodeCreateView.as_view(), name='recode_create'),
    path('recode/delete/<int:pk>', views.RecodeDeleteView.as_view(), name='recode_delete'),
]
