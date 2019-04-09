from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
import pytz

from . import models, serializers
from users.models import User  # 임시

KST = pytz.timezone('Asia/Seoul')


def check_car_status(func):
    def decorator(*args, **kwargs):
        now = datetime.datetime.now().replace(tzinfo=KST)
        ongoing_cars = models.Car.objects.filter(status='ongoing')
        for ongoing_car in ongoing_cars:
            if ongoing_car.auction_end_time <= now:
                ongoing_car.status = 'end'
                ongoing_car.save()
        return func(*args, **kwargs)

    return decorator


class CarCreateView(APIView):
    # 유저가 처음 자동차를 등록할 때, 모델명 리스트 리턴
    def get(self, request):
        car_models = models.Model.objects.all()
        serializer = serializers.ModelSerializer(car_models, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # user = request.user
        # 이후 변경 필요
        user = User.objects.get(id=1)
        car_images = request.FILES.getlist('car_images')
        if len(car_images) < 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_name = request.data.get('model')
        found_model = get_object_or_404(models.Model, name=model_name)
        serializer = serializers.CarSerializer(data=request.data, context={'images': car_images}, partial=True)
        if serializer.is_valid():
            saved_car = serializer.save(owner=user, model=found_model)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, car_id):
        found_car = get_object_or_404(models.Car, id=car_id, status='waiting')
        found_car.status = 'ongoing'

        now = datetime.datetime.now().replace(tzinfo=KST)
        found_car.auction_start_time = now
        forty_eight_hour_later = now + datetime.timedelta(hours=48)
        found_car.auction_end_time = forty_eight_hour_later.replace(tzinfo=KST)
        found_car.save()
        return Response(status=status.HTTP_200_OK)


class CarDetailView(APIView):

    @check_car_status
    def get(self, reqeust, car_id):
        found_car = get_object_or_404(models.Car, id=car_id)
        serializer = serializers.CarDetailSerializer(found_car)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CarListView(APIView):

    @check_car_status
    def get(self, request):
        model_name = request.GET.get('model', None)
        ordering = request.GET.get('ordering', None)
        if model_name is None:
            if ordering is None:
                cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end'))
            elif ordering == 'reverse':
                cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')).reverse()
        else:
            found_model = models.Model.objects.get(name=model_name)
            if ordering is None:
                cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')).filter(Q(model=found_model))
            elif ordering == 'reverse':
                cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')).filter(
                    Q(model=found_model)).reverse()
        paginator = Paginator(cars, 16)
        page = request.GET.get('page')
        cars = paginator.get_page(page)
        serializer = serializers.CarListSerializer(cars, many=True)
        # serializer.data.update({'car_total_count':len(cars),})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SearchView(APIView):

    @check_car_status
    def get(self, request):
        brand_name = request.GET.get('brand', None)
        kind_name = request.GET.get('kind', None)

        if brand_name is None and kind_name is None:
            brands = models.Brand.objects.all()
            serializer = serializers.BrandSerializer(brands, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif brand_name and kind_name is None:
            brand = models.Brand.objects.get(name=brand_name)
            kinds = models.Kind.objects.filter(brand=brand)
            serializer = serializers.KindSerializer(kinds, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif brand_name is None and kind_name:
            kind = models.Kind.objects.get(name=kind_name)
            car_models = models.Model.objects.filter(kind=kind)
            serializer = serializers.ModelSerializer(car_models, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

