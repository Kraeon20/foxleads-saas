from django.shortcuts import render
from .models import StateData  # Assuming you have a model named StateData for your MongoDB collection

from django.db.models import Count

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

# views.py

from django.http import JsonResponse

def get_cities_and_area_codes(request):
    state = request.GET.get('state', None)
    if state:
        # Query your database to fetch cities and area codes based on the selected state
        cities = StateData.objects.filter(state=state).values_list('city', flat=True).distinct()
        area_codes = StateData.objects.filter(state=state).values_list('area_code', flat=True).distinct()
        return JsonResponse({'cities': list(cities), 'areaCodes': list(area_codes)})
    else:
        return JsonResponse({'error': 'State parameter is missing'}, status=400)

