from django.db import models

# Create your models here.

class DiseaseIncident(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_detected = models.DateTimeField(auto_now_add=True)




class users_data(models.Model):
    user_name = models.CharField(max_length=255, null=True)
    user_email = models.EmailField(null=True)

    def __str__(self):
        return f'{self.user_name} - {self.user_email} '