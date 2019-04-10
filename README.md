## API Documentation
* 굵은 글씨로 표시된 Key는 필수값
* 사용자 인증은 JWT를 이용
    - Header의 Authorization Key에 JWT <your_token>를 추가하여 request
    - ex) JWT eyJ0eXAiOiJKV1QiLCJh
    - 관련 문서: [Django REST framework JWT](http://getblimp.github.io/django-rest-framework-jwt/)

## API 목록
* User
* Car

### Signip(Registration)
회원가입
* URL
`POST /diary/startchat/`

    - Headers
  Key: HASH
  Value: SE69KdAOBIMtjS6kZovvrOcmn2hrzO2DlVih6u4o (유저 고유 Hash)