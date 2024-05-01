from django.shortcuts import render
from .models import StateData  # Assuming you have a model named StateData for your MongoDB collection
from django.http import JsonResponse
from django.db.models import Count, Avg
import random

def dashboard(request):
    # Fetch distinct states
    distinct_states = StateData.objects.values('state').annotate(total=Count('state'))
    distinct_cities = StateData.objects.values('city').annotate(total=Count('city'))
    distinct_area_codes = StateData.objects.values('area_code').annotate(total=Count('area_code'))

    # Pass distinct states to the template
    context = {'distinct_states': distinct_states,
               'distinct_cities': distinct_cities,
               'distinct_area_codes': distinct_area_codes,}

    return render(request, 'dashboard.html', context)


def get_cities_and_area_codes(request):
    state = request.GET.get('state', None)
    if state:
        # Query your database to fetch cities and area codes based on the selected state
        cities = StateData.objects.filter(state=state).values_list('city', flat=True).distinct()
        return JsonResponse({'cities': list(cities)})
    else:
        return JsonResponse({'error': 'State parameter is missing'}, status=400)


def get_area_codes(request):
    city = request.GET.get('city', None)
    if city:
        # Query your database to fetch cities and area codes based on the selected state
        area_codes = StateData.objects.filter(city=city).values_list('area_code', flat=True).distinct()
        return JsonResponse({'areaCodes': list(area_codes)})
    else:
        return JsonResponse({'error': 'City parameter is missing'}, status=400)


def get_random_numbers(request):
    state = request.GET.get('state', None)
    city = request.GET.get('city', None)
    area_code = request.GET.get('area_code', None)
    num_of_numbers = int(request.GET.get('numOfNumbers', 1))

    if state or city or area_code:
        numbers = []
        for _ in range(num_of_numbers):
            if state and city and area_code:
                number = f"{area_code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            elif state and city:
                area_codes = StateData.objects.filter(city=city).values_list('area_code', flat=True).distinct()
                area_code = random.choice(list(area_codes))
                number = f"{area_code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            elif state:
                cities = StateData.objects.filter(state=state).values_list('city', flat=True).distinct()
                city = random.choice(list(cities))
                area_codes = StateData.objects.filter(city=city).values_list('area_code', flat=True).distinct()
                area_code = random.choice(list(area_codes))
                number = f"{area_code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            else:
                area_codes = StateData.objects.values_list('area_code', flat=True).distinct()
                area_code = random.choice(list(area_codes))
                number = f"{area_code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            numbers.append(number)
        return JsonResponse({'numbers': numbers})
    else:
        return JsonResponse({'error': 'State, City, or Area Code parameter is missing'}, status=400)