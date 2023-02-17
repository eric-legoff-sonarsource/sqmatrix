from django.urls import path

from . import views

urlpatterns = [
    path('', views.releases, name='releases'),
    path('plugins/', views.plugins, name='plugins'),
    path('add/', views.add, name='add'),
    path('compare/', views.compare, name='compare'),
]