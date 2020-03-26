from django.contrib import admin
from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.index, name='index'),
    path('championship/reset/', views.reset_championship_postions, name='reset_championship'),
    path('championship/standings/', views.championship_standings, name='championship_standings'),
    path('championship/racers/', views.championship_racers, name='championship_racers'),
    path('championship/<slug:the_slug>/', views.championship, name='championship'),
    ]
