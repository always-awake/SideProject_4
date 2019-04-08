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



class CarCreateAPIView(APIView):
    # 유저가 처음 자동차를 등록할 때, 모델명 리스트 리턴
    def get(self, request, format=None):
        car_models = models.Model.objects.all()
        serializer = serializers.ModelSerializer(car_models, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
            
    def post(self, request, format=None):
        #user = request.user
        # 이후 변경 필요
        user = User.objects.get(id=1)
        car_images = request.FILES.getlist('car_images')
        model_name = request.data.get('model')
        found_model = get_object_or_404(models.Model, name=model_name)
        serializer = serializers.CarSerializer(data=request.data, context={'images': car_images}, partial=True)
        if serializer.is_valid():
            saved_car = serializer.save(owner=user, model = found_model)
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


class CarDetailAPIView(APIView):

    def get(self, reqeust, car_id, format=None):
        found_car = get_object_or_404(models.Car, id=car_id)
        serializer = serializers.CarDetailSerializer(found_car)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CarListAPIView(APIView):

    def get(self, request, format=None):
        ordering = request.GET.get('ordering', None)
        if ordering == 'reverse':
            cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')).reverse()
        else:
            cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')) 

        paginator = Paginator(cars, 16)
        page = request.GET.get('page')
        cars = paginator.get_page(page)
        serializer = serializers.CarListSerializer(cars, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        