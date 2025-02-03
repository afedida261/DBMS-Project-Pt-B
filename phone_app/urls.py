from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('add_application', views.add_application, name='add_application'),
    path('remove_application', views.remove_application, name='remove_application'),
    path('install_application', views.install_application, name='install_application'),
    path('query_results', views.query_results, name='query_results')
]