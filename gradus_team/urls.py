from django.urls import path, include
from . import views

app_name = 'gradus_team'

urlpatterns = [
    path('', views.GradusHome.as_view(), name='home'),
    path('game/<int:pk>/', views.ShowGame.as_view(), name='show_game'),
    path('team/<slug:slug_team>/', views.ShowTeam.as_view(), name='show_team'),
    path('player/<slug:slug_player>/', views.ShowPlayer.as_view(), name='show_player'),
]

