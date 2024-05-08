import csv
import json
import random
import asyncio
import requests
from .models import StateData
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache


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
    


async def validate_number(request):
    number = request.GET.get('number')

    # Check if data is cached
    cached_data = cache.get(number)

    if cached_data:
        # If cached data exists, return it
        return JsonResponse(cached_data)

    # If data is not cached, make API request with a 1-second delay
    url = "https://reverse-phone-api.p.rapidapi.com/3.1/phone"
    querystring = {"phone": number}
    headers = {
        "X-RapidAPI-Key": "8da8c58121mshf9dd7599ee5bd69p115cffjsn437aaaa9f075",
        "X-RapidAPI-Host": "reverse-phone-api.p.rapidapi.com"
    }

    try:
        # Introduce a 1-second delay before making the API request
        await asyncio.sleep(1)
        
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Extract required details from API response
        phone_number = data.get('phone')
        is_valid = data.get('is_valid')
        line_type = data.get('line_type')
        carrier = data.get('carrier')
        is_prepaid = data.get('is_prepaid')

        # Store data in cache for 1 minute
        cache.set(number, {
            'phone_number': phone_number,
            'is_valid': is_valid,
            'line_type': line_type,
            'carrier': carrier,
            'is_prepaid': is_prepaid
        }, timeout=60)

        # Return the fetched data
        return JsonResponse({
            'phone_number': phone_number,
            'is_valid': is_valid,
            'line_type': line_type,
            'carrier': carrier,
            'is_prepaid': is_prepaid
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




import csv
from io import StringIO

def validate_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if file.name.endswith('.txt'):
            numbers = parse_txt_file(file)
        elif file.name.endswith('.csv'):
            numbers = parse_csv_file(file)
        else:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)
        validation_results = []
        for number in numbers:
            validation_result = validate_number({'GET': {'number': number}})
            validation_results.append(validation_result)
        return JsonResponse({'results': validation_results})
    else:
        return JsonResponse({'error': 'File not provided'}, status=400)

def parse_txt_file(file):
    numbers = []
    for line in file:
        number = line.strip()
        numbers.append(number)
    return numbers

def parse_csv_file(file):
    numbers = []
    csv_reader = csv.reader(StringIO(file.read().decode('utf-8')))
    for row in csv_reader:
        if row:  # Skip empty rows
            number = row[0].strip()  # Assuming the phone number is in the first column
            numbers.append(number)
    return numbers


def validate_file(request):
    if request.method == 'POST' and request.FILES['file']:
        # Read the uploaded file
        uploaded_file = request.FILES['file']

        # Parse the CSV file and extract numbers
        numbers = []
        reader = csv.reader(uploaded_file)
        for row in reader:
            numbers.extend(row)

        # Send numbers for validation
        validation_results = []
        for number in numbers:
            validation_result = validate_number(number)
            validation_results.append(validation_result)

        return JsonResponse({'validation_results': validation_results})
    else:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
