from djongo import models

class StateData(models.Model):
    area_code = models.IntegerField(db_column='area-code')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        db_table = 'states_cities_and_areacodes'



class GoogleScrapedData(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    website = models.URLField()
    phone_number = models.CharField(max_length=20)
    reviews_count = models.IntegerField()
    reviews_average = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'google_scraped_data'