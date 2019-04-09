from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'id',
            'image',
            'represent',
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = (
            'id',
            'name',
            'car_count',
            )


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Kind
        fields = (
            'id',
            'name',
            'car_count',
            )


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = (
            'id',
            'name',
            'car_count',
        )

class CarSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Car
        fields = (
            'id',
            'year',
            'fuel_type',
            'transmission_type',
            'color',
            'mileage',
            'address',
            'images',
        )

    def create(self, validated_data):
        images = self.context.get('images')
        car = models.Car.objects.create(**validated_data)
        for image in images:
            if not car.images.all(): 
                models.Image.objects.create(car=car, image=image, represent=True)
            else: 
                models.Image.objects.create(car=car, image=image)
        return car


class CarDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    kind = KindSerializer()
    model = ModelSerializer()
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Car
        fields = (
            'status',
            'id',
            'time_remaining',
            'brand',
            'kind',
            'model',
            'car_detail_year',
            'car_detail_mileage',
            'car_detail_info',
            'address',
            'images',
        )


class CarListSerializer(serializers.ModelSerializer):
    kind = KindSerializer()
    model = ModelSerializer()
    representative_image = ImageSerializer(read_only=True)

    class Meta:
        model = models.Car
        fields = (
            'status',
            'time_remaining',
            'id',
            'representative_image',
            'kind',
            'model',
            'car_detail_year',
            'car_list_mileage',
            'address',
        )