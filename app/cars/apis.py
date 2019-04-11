from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import datetime
import openpyxl 
import pytz
import random

from . import models, serializers


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

    def post(self, request):
        user = request.user
        car_images = request.FILES.getlist('car_images')
        if len(car_images) < 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_name = request.data.get('model')
        found_model = get_object_or_404(models.Model, model_name=model_name)
        serializer = serializers.CarSerializer(data=request.data, context={'images': car_images}, partial=True)
        if serializer.is_valid():
            saved_car = serializer.save(owner=user, model=found_model)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, car_id):
        if request.user.is_superuser:
            found_car = get_object_or_404(models.Car, id=car_id, status='waiting')
            if found_car.status == 'waiting':
                found_car.status = 'ongoing'

                now = datetime.datetime.now().replace(tzinfo=KST)
                found_car.auction_start_time = now
                forty_eight_hour_later = now + datetime.timedelta(hours=48)
                found_car.auction_end_time = forty_eight_hour_later.replace(tzinfo=KST)
                found_car.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
            found_model = models.Model.objects.get(model_name=model_name)
            if ordering is None:
                cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')).filter(Q(model=found_model))
            elif ordering == 'reverse':
                cars = models.Car.objects.filter(Q(status='ongoing') | Q(status='end')).filter(
                    Q(model=found_model)).reverse()
        paginator = Paginator(cars, 16)
        page = request.GET.get('page')
        cars = paginator.get_page(page)
        serializer = serializers.CarListSerializer(cars, many=True)
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
            brand = models.Brand.objects.get(brand_name=brand_name)
            kinds = models.Kind.objects.filter(brand=brand)
            serializer = serializers.KindSerializer(kinds, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif brand_name is None and kind_name:
            kind = models.Kind.objects.get(kind_name=kind_name)
            car_models = models.Model.objects.filter(kind=kind)
            serializer = serializers.ModelSerializer(car_models, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 브랜드(Brand), 차종(Kind), 모델(Model) 정보를 import 하고, 차량(Car) 더비 데이터를 생성하는 API
class TestView(APIView):

    def post(self, request):
        car_data = openpyxl.load_workbook('./car_data/brand_kind_model.xlsx')
        car_sheet = car_data.get_sheet_by_name('Sheet1')

        #브랜드(brand) 등록
        brand_name_list = []
        brand_list = list(car_sheet['A'])
        del brand_list[0]
        for brand in brand_list:
            if brand.value not in brand_name_list:
                brand_name_list.append(brand.value) 
        for brand_name in brand_name_list:
            brand = models.Brand()
            brand.brand_name = brand_name
            brand.save()
        
        # 차종(kind)등록
        brand_kind_list = []
        kind_list = []
        for row in car_sheet.rows:
            brand = row[0].value
            kind = row[1].value
            brand_kind_list.append((brand, kind))
        del brand_kind_list[0]
        for brand_kind in brand_kind_list:
            if brand_kind[1] not in kind_list:
                kind_list.append(brand_kind[1])
                brand = models.Brand.objects.get(brand_name=brand_kind[0])
                kind = models.Kind()
                kind.brand = brand
                kind.kind_name = brand_kind[1]
                kind.save()        

        # 모델(model)등록
        kind_model_list = []
        model_list = []
        for row in car_sheet.rows:
            kind = row[1].value
            model = row[2].value
            kind_model_list.append((kind, model))
        del kind_model_list[0]
        for kind_model in kind_model_list:
            kind = models.Kind.objects.get(kind_name=kind_model[0])
            model = models.Model()
            model.kind = kind
            model.model_name = kind_model[1]
            model.save()
            model_list.append(kind_model[1])
        car_data.close()

        # Car 더미 데이터 생성
        owner = request.user
        i = 0
        while i < 500:
            fuel_type_list = ['lpg', '휘발유', '디젤', '하이브리드', '전기', '바이퓨얼']
            transmission_type_list = ['오토', '수동']
            mileage_list = ['25000', '10000', '2000','6500']
            address_list = ['서울 영등포구', '서울 관악구', '서울 종로구', '서울 강남구']
            color_list = ['흰색', '검정', '은색', '쥐색', '빨강색', '노랑색']
            model = models.Model.objects.get(model_name=random.choice(model_list))
            car = models.Car()
            car.owner = owner
            car.model = model
            car.year = '2018-02-03'
            car.fuel_type = random.choice(fuel_type_list)
            car.transmission_type = random.choice(transmission_type_list)
            car.mileage = random.choice(mileage_list)
            car.address = random.choice(address_list)
            car.color = random.choice(color_list)
            car.save()
            j = 0
            while j < 5: 
                image = models.Image()
                image.car = car
                if j == 0:
                    image.represent = True
                else:
                    image.represent = False
                image.image = 'tests/PRND.png'
                image.save()
                j += 1
            i += 1        

        # Car데이터 500중 200개는 ongoing, 200개는 end, 100개는 waiting으로 설정
        i = 1
        # ongoing
        while i < 201:
            car = models.Car.objects.get(id=i)
            car.status = 'ongoing'
            now = datetime.datetime.now().replace(tzinfo=KST) + datetime.timedelta(minutes=1)
            car.auction_start_time = now
            forty_eight_hour_later = now + datetime.timedelta(hours=48)
            car.auction_end_time = forty_eight_hour_later.replace(tzinfo=KST)
            car.save()
            i += 1

        # status 값이 1분 후에 자동으로 end로 변경
        while i < 401:
            car = models.Car.objects.get(id=i)
            car.status = 'ongoing'
            now = datetime.datetime.now().replace(tzinfo=KST)
            car.auction_start_time = now
            one_minute_later = now + datetime.timedelta(minutes=1)
            car.auction_end_time = one_minute_later.replace(tzinfo=KST)
            car.save()
            i += 1
        return Response(status=status.HTTP_200_OK)