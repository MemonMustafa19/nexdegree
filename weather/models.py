from django.db import models

# Create your models here.


class WeatherRecord(models.Model):
    curr_weather = models.CharField(max_length=255)