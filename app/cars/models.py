from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
import datetime
from pytz import timezone


class TimeStampedModel(models.Model):
    """ Base Model """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimeStampedModel):
    """ Brand Model """
    brand_name = models.CharField(max_length=50)

    @property
    def car_count(self):
        car_count = 0
        kinds = self.kinds.all()
        for kind in kinds:
            car_count += kind.car_count 
        return car_count

    def __str__(self):
        return f'{self.brand_name}'


class Kind(TimeStampedModel):
    """ Kind Model """
    kind_name = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, related_name='kinds', on_delete=models.CASCADE)

    @property
    def car_count(self):
        car_count = 0
        models = self.models.all()
        for model in models:
            car_count += model.car_count 
        return car_count

    def __str__(self):
        return f'{self.kind_name}'


class Model(TimeStampedModel):
    """ Model Model """
    model_name = models.CharField(max_length=50)
    kind = models.ForeignKey(Kind, related_name='models', on_delete=models.CASCADE)

    @property
    def car_count(self):
        return self.cars.all().count()
    
    def __str__(self):
        return f'{self.model_name}'


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
    model = models.ForeignKey(Model, related_name='cars', on_delete=models.CASCADE)
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
    def brand(self):
        return self.model.kind.brand
    
    @property
    def kind(self):
        return self.model.kind

    @property
    def car_detail_year(self):
        return f'{self.year.strftime("%Y-%m")} ({self.year.strftime("%Y")}년형)'

    @property
    def car_detail_mileage(self):
        return f'{intcomma(self.mileage)}km'

    @property
    def car_detail_info(self):
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
    def car_list_mileage(self):
        return f'{self.mileage/10000}만km'

    def __str__(self):
        return f'{self.id}-{self.kind}/{self.model}'
    
    class Meta:
        ordering = ['-auction_start_time']

    
class Image(TimeStampedModel):
    """ Image Model """
    image = models.ImageField(upload_to=f'cars/{datetime.datetime.now().strftime("%Y-%m-%d")}', null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    represent = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'{self.car.id}-{self.car.model}'
