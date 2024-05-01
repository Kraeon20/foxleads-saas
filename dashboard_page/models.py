from djongo import models

class StateData(models.Model):
    area_code = models.IntegerField(db_column='area-code')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        db_table = 'states_cities_and_areacodes'