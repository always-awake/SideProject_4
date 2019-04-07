from django.conf import settings
from django.db import models
import datetime


class TimeStampedModel(models.Model):
    """ Base Model """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Car(TimeStampedModel):
    """ Car Model """
    FUEL_CHOICES = (
        ('lpg', 'LPG'),
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
        ('bifuel', 'Bifuel'),
    )

    TRANSMISSION_CHOICES = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )

    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('onging', 'Onging'),
        ('end', 'End'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cars', on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    kind = models.CharField(max_length=80, null=True)
    model = models.CharField(max_length=80, null=True)
    year = models.DateField(auto_now=False, auto_now_add=False)
    fuel_type = models.CharField(max_length=80, choices=FUEL_CHOICES, null=True)
    transmission_type = models.CharField(max_length=80, choices=TRANSMISSION_CHOICES, null=True)
    mileage = models.IntegerField()
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=80, choices=STATUS_CHOICES, null=True, default='waiting')
    auction_start_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    auction_end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.brand}/{self.model}'
    
    class Meta:
        ordering = ['-auction_end_time']

    
class Image(TimeStampedModel):
    """ Image Model """
    image = models.ImageField(upload_to=f'cars/{datetime.datetime.today()}', null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.car.brand}/{self.car.model}'