from django.urls import path

from . import apis

app_name = 'cars'
urlpatterns = [
    path('', apis.CarListAPIView.as_view(), name='main_car'),
    path('new/', apis.CarAPIView.as_view(), name='create_car'),
    path('<int:car_id>/', apis.CarAPIView.as_view(), name='detail_car'),
    path('<int:car_id>/approval/', apis.CarAPIView.as_view(), name='modify_car_status'),

]
