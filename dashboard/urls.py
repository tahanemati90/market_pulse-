from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chart-data/<str:symbol>/', views.live_chart_data, name='live_chart_data'),
]
