from django.urls import path

from . import apis

app_name = 'cars'
urlpatterns = [
    path('', apis.CarListView.as_view(), name='car_list'),
    path('new/', apis.CarCreateView.as_view(), name='car_new'),
    path('<int:car_id>/', apis.CarDetailView.as_view(), name='car_detail'),
    path('<int:car_id>/approval/', apis.CarCreateView.as_view(), name='car_modify_status'),
    path('search/', apis.SearchView.as_view(), name='search'),

    path('test/', apis.TestView.as_view(), name='test'),
]
