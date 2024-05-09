from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/cities/', views.get_cities_and_area_codes, name='get_cities_and_area_codes'),
    path('api/area-codes', views.get_area_codes, name='get_area_codes'),
    path('api/get-random-numbers', views.get_random_numbers, name='get_random_numbers'),
    path('api/validate-number/', views.validate_number, name='validate_number'),
    path('api/validate-number-in-file', views.validate_number, name='validate_number'),
    path('google-scraper/', views.google_scraper, name='google_craper'),
    path('scrape-google-maps/', views.scrape_google_maps_data, name='scrape_google_maps'),

]