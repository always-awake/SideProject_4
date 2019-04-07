from django.urls import path

from . import apis

app_name = 'cars'
urlpatterns = [
    path('new/', apis.CarCreateAPIView.as_view(), name='create_car'),
]
