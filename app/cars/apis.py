from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from . import models, serializers
from users.models import User


class CarCreateAPIView(APIView):
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
