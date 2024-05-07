# In yourapp/management/commands/insert_data.py

from django.core.management.base import BaseCommand
from dashboard_page.models import State, City, AreaCode
import json

class Command(BaseCommand):
    help = 'Insert data into MongoDB'

    def handle(self, *args, **kwargs):
        with open('data.json', 'r') as file:
            data = json.load(file)

        for state_data in data:
            state = State.objects.create(name=state_data['state'])
            for city_name in state_data['cities']:
                city = City.objects.create(name=city_name, state=state)
                for area_code in state_data['area_codes']:
                    AreaCode.objects.create(code=area_code, city=city)

        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
