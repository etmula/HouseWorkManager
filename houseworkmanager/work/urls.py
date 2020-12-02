from django.urls import path
from . import views

app_name = 'work'
urlpatterns = [
    path('composites/<int:pk>', views.CompositeListView.as_view(), name='composite_list'),
    path('composites/<int:pk>/create', views.CompositeCreateView.as_view(), name='composite_create'),
    path('composites/update/<int:pk>', views.CompositeUpdateView.as_view(), name='composite_update'),
    path('composites/delete/<int:pk>', views.CompositeDeleteView.as_view(), name='composite_delete'),
    path('works/<int:pk>', views.WorkDetailView.as_view(), name='work_detail'),
    path('works/<int:pk>/work-exected-recodes', views.WorkExectedRecodeListView.as_view(), name='work_workexectedrecode_list'),
    path('works/<int:pk>/create', views.WorkCreateView.as_view(), name='work_create'),
    path('works/update/<int:pk>', views.WorkUpdateView.as_view(), name='work_update'),
    path('works/delete/<int:pk>', views.WorkDeleteView.as_view(), name='work_delete'),
    path('work-exected-recodes/', views.WorkExectedRecodeListView.as_view(), name='workexectedrecode_list'),
    path('work-exected-recodes/<int:pk>', views.WorkExectedRecodeDetailView.as_view(), name='workexectedrecode_detail'),
    path('work-exected-recodes/create', views.WorkExectedRecodeCreateView.as_view(), name='workexectedrecode_create'),
    path('work-exected-recodes/delete/<int:pk>', views.WorkExectedRecodeDeleteView.as_view(), name='workexectedrecode_delete'),

]
