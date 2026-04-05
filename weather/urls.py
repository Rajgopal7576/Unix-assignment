from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/', views.remove_favorite, name='remove_favorite'),
]
