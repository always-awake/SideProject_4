from django.urls import path

from . import apis

app_name = 'cars'
urlpatterns = [
    path('', apis.CarListAPIView.as_view(), name='car_list'),
    path('new/', apis.CarCreateAPIView.as_view(), name='car_new'),
    path('<int:car_id>/', apis.CarDetailAPIView.as_view(), name='car_detail'),
    path('<int:car_id>/approval/', apis.CarCreateAPIView.as_view(), name='car_modify_status'),

]
