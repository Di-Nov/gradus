from django.urls import path, include
from . import views

app_name = 'gradus_team'

urlpatterns = [
    path('/', views),

]