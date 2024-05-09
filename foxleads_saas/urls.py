"""
URL configuration for foxleads_saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard_page.views import dashboard
from dashboard_page.views import (dashboard, 
                                    get_cities_and_area_codes, 
                                    get_area_codes, 
                                    get_random_numbers, 
                                    validate_number, 
                                    google_scraper,
                                    # scrape_google_maps
                                    scrape_google_maps_data)


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('landing_page.urls')),
    path('', dashboard, name='dashboard'),
    path('api/cities/', get_cities_and_area_codes, name='get_cities_and_area_codes'),  # Include the API endpoint
    path('api/area-codes/', get_area_codes, name='get_area_codes'),
    path('api/get-random-numbers', get_random_numbers, name='get_random_numbers'),
    path('api/validate-number/', validate_number, name='validate_number'),
    path('google-scraper/', google_scraper, name='google_scraper'),
    path('scrape-google-maps/', scrape_google_maps_data, name='scrape_google_maps'),


]
