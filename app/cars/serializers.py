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


class CarSerializer(serializers.ModelSerializer):
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
            'color',
            'mileage',
            'address',
            'images',
        )

    def create(self, validated_data):
        images = self.context.get('images')
        car = models.Car.objects.create(**validated_data)
        for image in images:
            # 등록된 첫번째 이미지는 대표 이미지로 설정
            if not car.images.all(): 
                models.Image.objects.create(car=car, image=image, represent=True)
            else: 
                models.Image.objects.create(car=car, image=image)
        return car


class CarDetailSerializer(serializers.ModelSerializer):
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
