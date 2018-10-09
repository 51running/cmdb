from django.urls import path
from asset import views

app_name = 'asset'
urlpatterns = [
    path('', views.index, name="index"),
    path('list/ajax', views.list_ajax, name="list_ajax"),
    path('view/ajax', views.view_ajax, name="view_ajax"),
    path('update/ajax', views.update_ajax, name="update_ajax"),
    path('delete/ajax', views.delete_ajax, name="delete_ajax"),
    path('resource/ajax', views.resource_ajax, name="resource_ajax"),
]
