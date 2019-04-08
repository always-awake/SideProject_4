from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from pytz import timezone
import pytz

from . import models, serializers
from users.models import User



class CarAPIView(APIView):

    def get(self, request, car_id, format=None):
        found_car = get_object_or_404(models.Car, id=car_id)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
            
    def post(self, request, format=None):
        #user = request.user
        # 이후 변경 필요
        user = User.objects.get(id=1)
        car_images = request.FILES.getlist('car_images')
        serializer = serializers.CarSerializer(data=request.data, context={'images': car_images}, partial=True)
        if serializer.is_valid():
            saved_car = serializer.save(owner=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, car_id, format=None):
        found_car = get_object_or_404(models.Car, id=car_id)
        found_car.status = 'ongoing'

        KST = pytz.timezone('Asia/Seoul')
        now = datetime.datetime.now().replace(tzinfo=KST)
        found_car.auction_start_time = now

        forty_eight_hour_later = now + datetime.timedelta(hours=48)
        found_car.auction_end_time = forty_eight_hour_later.replace(tzinfo=KST)
        found_car.save()
        return Response(status=status.HTTP_200_OK)


class CarListAPIView(APIView):

    def get(self, request, format=None):
        cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end'))
        paginator = Paginator(cars, 16)
        page = request.GET.get('page')
        print(page)
        cars = paginator.get_page(page)
        serializer = serializers.CarListSerializer(cars, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        