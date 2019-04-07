from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'id',
            'image',
        )


class CarSerializer(serializers.HyperlinkedModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

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

    def create(self, validated_data):
        images = self.context.get('images')
        car = models.Car.objects.create(**validated_data)
        for image in images:
            models.Image.objects.create(car=car, image=image)
        return car
