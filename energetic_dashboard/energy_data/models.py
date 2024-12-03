from django.db import models

class EnergyData(models.Model):
    date = models.DateField()
    region = models.CharField(max_length=255)
    consumption_twh = models.FloatField()

    def __str__(self):
        return f"{self.region} - {self.date} - {self.consumption_twh} TWh"
