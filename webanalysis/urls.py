from django.urls import path
from webanalysis import views

app_name = 'webanalysis'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('upload/', views.upload, name="upload"),
    path('dist_status_code/', views.dist_status_code, name="dist_status_code"),
    path('trend_visit/', views.trend_visit, name="trend_visit"),
    path('devops/user/', views.devops_user, name="devops_user"),
]

