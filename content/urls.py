from django.contrib import admin
from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.index, name='index'),
    path('championship/reset/', views.reset_championship_postions, name='reset_championship'),
    path('championship/standings/', views.championship_standings, name='championship_standings'),
    path('championship/standings/<int:see_full>', views.championship_standings, name='championship_standings_full'),
    path('championship/racers/', views.championship_racers, name='championship_racers'),
    path('championship/<slug:the_slug>/', views.championship_index, name='championship_index'),
    path('championship/event/<slug:the_slug>/', views.championship, name='championship'),
    path('team/', views.team, name='team'),
    path('documentation/', views.documentation, name='documentation'),
    path('corporate/', views.corporate, name='corporate'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('join/', views.join, name='join'),
    path('news/', views.news, name='news'),
    path('training/centres', views.training_centres, name='training_centres'),
    ]
