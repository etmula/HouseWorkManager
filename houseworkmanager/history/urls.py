from django.urls import path

from . import views

app_name = 'history'
urlpatterns = [
    path('recode/', views.RecodeListView.as_view(), name='recode_list'),
    path('report/<int:year>/<int:month>', views.RecodeListMonthlyView.as_view(), name='recode_list_monthly'),
    path('recode/detail/<int:pk>', views.RecodeDetailView.as_view(), name='recode_detail'),
    path('recode/create', views.RecodeCreateView.as_view(), name='recode_create'),
    path('recode/delete/<int:pk>', views.RecodeDeleteView.as_view(), name='recode_delete'),
]
