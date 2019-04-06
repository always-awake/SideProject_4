from rest_framework import serializers

from . import models


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        fields = (
            'id',
            'brand',
            'kind',
            'model',
            'year',
            'fuel_type',
            'transmission_type',
            'mileage',
            'address',
            'images',
        )
