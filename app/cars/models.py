from django.conf import settings
from django.db import models
import datetime
from pytz import timezone


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
        ('휘발유', 'Gasoline'),
        ('디젤', 'Diesel'),
        ('하이브리드', 'Hybrid'),
        ('전기', 'Electric'),
        ('바이퓨얼', 'Bifuel'),
    )

    TRANSMISSION_CHOICES = (
        ('오토', 'Auto'),
        ('수동', 'Manual'),
    )

    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('ongoing', 'Ongoing'),
        ('end', 'End'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cars', on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    kind = models.CharField(max_length=80, null=True)
    model = models.CharField(max_length=80, null=True)
    year = models.DateField(auto_now=False, auto_now_add=False)
    fuel_type = models.CharField(max_length=80, choices=FUEL_CHOICES, null=True)
    transmission_type = models.CharField(max_length=80, choices=TRANSMISSION_CHOICES, null=True)
    color = models.CharField(max_length=30, null=True)
    mileage = models.IntegerField()
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=80, choices=STATUS_CHOICES, null=True, default='waiting')
    auction_start_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    auction_end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    @property
    def detail_car_year(self):
        return f'{self.year.strftime("%Y-%m")} ({self.year.strftime("%Y")}년형)'

    @property
    def detail_car_mileage(self):
        return f'{self.mileage}km'

    @property
    def detail_car_info(self):
        return f'{self.fuel_type}·{self.transmission_type}·{self.color}'

    @property
    def time_remaining(self):
        if self.status == 'ongoing':
            KST = timezone('Asia/Seoul')
            how_long = self.auction_end_time - datetime.datetime.now().replace(tzinfo=KST)
            days, seconds = how_long.days, how_long.seconds
            hours = days * 24 + seconds // 3600
            mins = (seconds % 3600) // 60
            seconds = seconds % 60
            return f'{hours}:{mins}:{seconds}'
        else: 
            return None
    
    @property
    def representative_image(self):
        return self.images.all().get(represent=True)

    @property
    def car_list_mileage_ten_thousand(self):
        return f'{self.mileage/10000}만km'

    def __str__(self):
        return f'{self.id} - {self.brand}/{self.model}'
    
    class Meta:
        ordering = ['-auction_start_time']

    
class Image(TimeStampedModel):
    """ Image Model """
    image = models.ImageField(upload_to=f'cars/{datetime.datetime.now().strftime("%Y-%m-%d")}', null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    represent = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'{self.car.brand}/{self.car.model}'