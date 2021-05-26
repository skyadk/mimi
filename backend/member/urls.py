from django.urls import path
from django.conf import settings
from .views import MemberView, SignView, MemberFix

urlpatterns = [
    #회원가입
    path("sign-up", MemberView.as_view({"post": "post"})),
    #중복확인 및 이메일 인증
    path("auth-email/<str:target_code>", MemberView.as_view({"get": "get"})),
    #로그인
    path("sign-in", SignView.as_view({"post": "post"})),
    #PW 찾기 이메일 인증
    path("find-auth-email/<str:target_code>", MemberFix.as_view({"get": "email_Check"})),
    #아이디 찾기
    path("find-id/<str:id>,<str:birthday>", MemberFix.as_view({"get": "find_Id"})),
    #PW 변경
    path("update-pw/<str:id>,<str:password>", MemberFix.as_view({"put": "change_Pw"})),

    path("aaa", MemberFix.as_view({"get": "aaa"}))
]