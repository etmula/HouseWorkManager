from django.urls import path

from . import views

app_name = 'stats'
urlpatterns = [
    path('score-user/<int:year>/<int:month>', views.score_user_line, name='score_user'),
    path('work-exected/<int:year>/<int:month>', views.work_exected_column, name='work_exected'),
]
