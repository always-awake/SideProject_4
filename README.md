API Documentation
=================
### **테스트 시, 회원가입 후 -> 테스트 API를 이용해 더미 데이터를 생성하고 테스트하시면 됩니다.**
#
* **굵은 글씨**로 표시된 Key는 필수값
* 사용자 인증은 JWT를 이용
    - Header의 Authorization Key에 JWT <your_token>를 추가하여 request
    - ex) JWT eyJ0eXAiOiJKV1QiLCJh
    - 관련 문서: [Django REST framework JWT](http://getblimp.github.io/django-rest-framework-jwt/)
    - 회원 가입, 로그인 API 외에 모든 API는 Authenticate required


## API 목록
* 로그인 API
* 차종 검색 필터 목록 API 
* 차량 등록 API
* 경매 승인 API
* 차량 목록 API
* 차량 상세 API
* 사용된 데코레이터 설명
* 테스트 API

## 로그인 API
### Sign up(Registration)
> 회원가입
- Request</br>
`POST /users/registration/`

  * Body
    + **username**: user name (ex. 이미림)
    + **password1**: user password 
    + **password2**: user password (비밀번호 재확인을 위함)
    + email: user email

- Response</br>
//status: HTTP 201 Created
```
{
    "token": "<your_token>",
    "user": {
        "pk": 1,
        "username": "이미림",
        "email": "leemirim@gmail.com",
        "first_name": "",
        "last_name": ""
    }
}
```

### Login
> 로그인(토큰 생성)
- Request</br>
`POST /users/login/`

  * Body
    + **username**: user name
    + **password**: user password

- Response</br>
//status: HTTP 200 OK
```
{
    "token": "<your_token>",
    "user": {
        "pk": 1,
        "username": "이미림",
        "email": "leemirim@gmail.com",
        "first_name": "",
        "last_name": ""
    }
}
```

### Logout
> 로그아웃
- Request</br>
`POST /users/logout/`

  * Header
    + **Authorization**: JWT <your_token>

- Response</br>

```
{
    "detail": "로그아웃되었습니다."
}
```

#
#### 참고
* 회원가입, 로그인, 로그아웃 기능은 [django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html#basic) 사용
* 회원 가입/로그인 시, email을 필수로 요구하지 않도록 설정 (config/settings/base.py)
```
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
```
#

## 차종 검색 필터 목록 API 
> 1. 단수 선택 </br>
> 2. Brand(브랜드/제조사) > kind(차종/등급) > model(모델) </br>
> 3. car_count는 해당 브랜드/차종/모델에 속해있는 차량의 수

### Brand List search
- Request</br>
`GET /cars/search/`

  * Params
    + None

  * Header
    + **Authorization**: JWT <your_token>

- Success Response</br>
//status: HTTP 200 OK
```
[
    {
        "id": 1,
        "brand_name": "현대",
        "car_count": 2
    },
    {
        "id": 2,
        "brand_name": "기아",
        "car_count": 0
    },
    {
        "id": 3,
        "brand_name": "벤츠",
        "car_count": 0
    },
    {
        "id": 4,
        "brand_name": "르노삼성",
        "car_count": 6
    }
]
```

### Kind List search
- Request</br>
`GET /cars/search/`

  * Params
    + **brand**: brand name (ex. 현대)
  * Header
    + **Authorization**: JWT <your_token>

- Response</br>
//status: HTTP 200 OK
```
[
    {
        "id": 1,
        "kind_name": "그랜저",
        "car_count": 0
    },
    {
        "id": 2,
        "kind_name": "소나타",
        "car_count": 2
    }
]
```


### Model List search
- Request</br>
`GET /cars/search/`

  * Params
    + **kind**: kind name (ex. 소나타)
  * Header
    + **Authorization**: JWT <your_token>

- Response</br>
//status: HTTP 200 OK
```
[
    {
        "id": 1,
        "model_name": "소나타 2.0",
        "car_count": 2
    }
]
```

## 차량 등록 API
### Car Create API
> 1. 자동차 등록 (차량이 등록되면 상태는 기본으로 승인 대기(status=waiting)입니다.)
> 2. model list는 'Model List 검색' API로 불러올 수 있음 (Model에 등록되지 않은 model로 Car 생성 불가)
- Requeast</br>
`POST /cars/new/`

  * Header
    + **Authorization**: JWT <your_token>
  * Body 
    - **model**: model name (ex. 소나타 2.0) 
    - **year**: yyyy-mm-dd 형식 (ex. 2018-12-25)
    - **fuel_type**: lpg, 휘발유, 디젤, 하이브리드, 전기, 바이퓨얼 중 하나
    - **transmission_type**: 오토, 수동 중 하나
    - **color**: color (ex. 은색)
    - **mileage**: mileage (ex. 25000)
    - **address**: address (ex. 서울 관악구)
    - **car_images**: ImageField/이미지 5장 이상
      + 5장 미만 사진 등록시 Bas Request응답 -> 오브젝트 생성x
      + 등록되는 첫 번째 사진은 대표사진(represent=True)으로 설정
      + 이미지들은 /media/cars/해당 오브젝트 생성일/ 파일에 저장됨

- Response</br>
//status: HTTP 201 Created
```
{
    "id": 1,
    "year": "2018-12-25",
    "fuel_type": "바이퓨얼",
    "transmission_type": "오토",
    "color": "은색",
    "mileage": 25000,
    "address": "서울 관악구",
    "images": [
        {
            "id": 35,
            "image": "/media/cars/2019-04-10/A.png",
            "represent": true
        },
        {
            "id": 36,
            "image": "/media/cars/2019-04-10/B.jpeg",
            "represent": false
        },
        {
            "id": 37,
            "image": "/media/cars/2019-04-10/C.jpeg",
            "represent": false
        },
        {
            "id": 38,
            "image": "/media/cars/2019-04-10/D.jpeg",
            "represent": false
        },
        {
            "id": 39,
            "image": "/media/cars/2019-04-10/E.jpeg",
            "represent": false
        }
    ]
}
```

## 경매 승인 API
> 1. car_id를 갖고 있는 Car 오브젝트가 있어야 하고, 해당 Car 오브젝트의 status의 값이 'waiting' 이어야 합니다.
> 2. superuser의 권한을 갖고 있어야 수행됩니다. 그 외의 유저가 request하면, UNAUTHORIZED 응답을 얻습니다.
- Request</br>
`PUT /cars/:Car_Id/approval/`

  * Header
    + **Authorization**: JWT <your_token>

- Response</br>
//status: HTTP 200 OK

## 차량 목록 API
### Car List API
> 1. 기본적으로 status가 'ongoing(경매 진행)' or 'end(경매 종료)'인 자동차(Car) 리스트를 '경매 시작 시간'을 기준으로 정렬하여 보여줍니다.
> 2. model params가 존재한다면, 검색 필터(모델에 속한 Car), 순서(정순, 역순)에 맞는 자동차(Car) 리스트를 보여줍니다. 
> 3. ordering params가 reverse 값을 갖고 있다면, 역순 리스트를 보여줍니다.
> 4. 페이지네이션을 지원: 한 페이지에 최대 16개의 자동차(Car)을 보여줍니다. page params에 원하는 페이지 번호를 입력하여 요청합니다.
> 5. 차종 검색 필터 목록 API와 함께 사용하면 필터링 기능이 가능합니다.

- Request</br>
`GET /cars/`

  * Params
    + model: model name or None (ex. sm5) (model에 속한 Car만을 보고 싶을 경우는 필수 필드)
    + ordering: reverse or None 
    + **page**: page number
  * Header
    + **Authorization**: JWT <your_token>

- Response</br>
  * Params
    - page:1
    - model: sm5
    
//status: HTTP 200 OK
```
[
    {
        "id": 4,
        "status": "ongoing",
        "time_remaining": "7:18:16",
        "representative_image": {
            "id": 15,
            "image": "/media/cars/2019-04-09/A.png",
            "represent": true
        },
        "kind": {
            "id": 4,
            "name": "sm",
            "car_count": 7
        },
        "model": {
            "id": 3,
            "name": "sm5",
            "car_count": 3
        },
        "car_detail_year": "1996-12 (1996년형)",
        "car_list_mileage": "2.5만km",
        "address": "서울 신도림"
    }
]

```
## 차량 상세 API
- Request</br>
`GET /cars/:Car_Id`

  * Header
    + **Authorization**: JWT <your_token>

- Response</br>
//status: HTTP 200 OK
```
{
    "id": 4,
    "status": "ongoing",
    "time_remaining": "7:4:5",
    "brand": {
        "id": 4,
        "name": "르노삼성",
        "car_count": 7
    },
    "kind": {
        "id": 4,
        "name": "sm",
        "car_count": 7
    },
    "model": {
        "id": 3,
        "name": "sm5",
        "car_count": 3
    },
    "car_detail_year": "1996-12 (1996년형)",
    "car_detail_mileage": "25,000km",
    "car_detail_info": "하이브리드·수동·흰색",
    "address": "서울 신도림",
    "images": [
        {
            "id": 15,
            "image": "/media/cars/2019-04-09/A.png",
            "represent": true
        },
        {
            "id": 16,
            "image": "/media/cars/2019-04-09/B.png",
            "represent": false
        },
        {
            "id": 17,
            "image": "/media/cars/2019-04-09/C.png",
            "represent": false
        },
        {
            "id": 18,
            "image": "/media/cars/2019-04-09/D.png",
            "represent": false
        },
        {
            "id": 19,
            "image": "/media/cars/2019-04-09/E.jpg",
            "represent": false
        }
    ]
}
```

## 데코레이터 
> cars/apis.py 안의 check_car_status 
```
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
```
* 경매 승인 후, 48시간 후에 경매가 자동으로 종료되어야 하기 때문에 time_remaining(경매 남은 시간) 필드가 보여거나, 필요한 요청을 할 때마다 check_car_status 데코레이터 호출
* 현재 시간과 status='ongoing'인 Car의 auction_end_time 값을 비교하여 status 값을 변경해준다.

-------------
## 테스트 API
> 1. 테스트를 위해 car_data폴더 속, 엑셀 데이터를 이용해 브랜드(Brand), 차종(Kind), 모델(Model) object 생성
> 2. Car object를 생성할 때, 각 필드는 랜덤으로 선택된 값으로 설정
> 3. Image object의 image필드는 모두 media/tests/PRND.png로 설정
> 4. 500개의 Car object를 생성
> 5. 200개 Car object는 '경매 종료 시간(auction_end_time)'을 현재 시간의 1분 후로 지정하여, 1분 후에 자동으로 status = 'end' 설정
> 6. 200개 Car object는 '경매 시작 시간(auction_start_time)'을 현재 시간의 1분 전으로 지정하고, status = 'ongoing' 설정 (경매 종료된 차량이 경매 진행중인 차량보다 경매 승인이 더 빠를 것이라 가정)
> 7. 나머지 100개는 어떠한 처리 x -> status = 'waiting' 기본으로 설정

- Request</br>
`POST /cars/test/`

  * Header
    + **Authorization**: JWT <your_token>

- Response</br>
//status: HTTP 200 OK

