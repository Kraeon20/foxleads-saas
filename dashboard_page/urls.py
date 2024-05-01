from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/cities/', views.get_cities_and_area_codes, name='get_cities_and_area_codes'),
]