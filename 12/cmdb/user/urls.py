from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('valid_login/', views.valid_login, name="valid_login"),
    path('logout/', views.logout, name="logout"),
    path('delete/', views.delete, name="delete"),
    path('view/', views.view, name="view"),
    path('update/', views.update, name="update"),
    path('insert_view/', views.insert_view, name="insert_view"),
    path('insert/', views.insert, name="insert"),
    path('find_view/', views.find_view, name="find_view"),
    path('find/', views.find, name="find"),
    path('passwd_view/', views.passwd_view, name="passwd_view"),
    path('passwd/', views.passwd, name="passwd"),
    path('nginx_log/', views.nginx_log, name="nginx_log"),
    path('insert/ajax', views.insert_ajax, name="insert_ajax"),
    path('delete/ajax', views.delete_ajax, name="delete_ajax"),
    path('view/ajax', views.view_ajax, name="view_ajax"),
    path('update/ajax', views.update_ajax, name="update_ajax"),
]
