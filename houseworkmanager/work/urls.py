from django.urls import path

from . import views

app_name = 'work'
urlpatterns = [
    path('work/', views.WorkListView.as_view(), name='work_list'),
    path('work/<int:pk>', views.WorkDetailView.as_view(), name='work_detail'),
    path('work/create', views.WorkCreateView.as_view(), name='work_create'),
    path('work/update/<int:pk>', views.WorkUpdateView.as_view(), name='work_update'),
    path('work/delete/<int:pk>', views.WorkDeleteView.as_view(), name='work_delete'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),
]
