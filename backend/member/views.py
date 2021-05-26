from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from django.http import Http404, HttpResponse, JsonResponse
from .models import Member
from .serializers import MemberSerializer, ChangeMemberPasswordSerializer, SearchMemberIdSerializer
from backend.settings import SECRET_KEY, EMAIL_HOST_USER
from .token import email_auth_num
from django.core.mail import EmailMessage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import json
import bcrypt
import jwt


#GenericViewSet -> get_queryset, get_object사용

# Create your views here.

#1. ID찾기, 2. PW찾기 - 이메일 중복여부 확인, 3. PW변경
class MemberFix(viewsets.ModelViewSet, View):
    
    def aaa(self, request):
        if Member.objects.filter(id = "ehdrjf337@gmail.com").exists():
                return JsonResponse({"message" : "EXISTS_ID"}, status=400)
        return JsonResponse({"message" : "aaa"}, status=200)
    #ID찾기
    def find_Id(self,request, id='', birthday=''):
        serializer_class = SearchMemberIdSerializer
        print(birthday)
        if Member.objects.filter(birthday = birthday).exists():
            #전체값에서 id와 birthday값 비교해야함
            print("날짜존재")
            if Member.objects.filter(id = id).exists():
                return JsonResponse({"message" : "EXISTS_ID"}, status=200)
            return JsonResponse({"message" : "NOT_EXISTS_ID"}, status=400)
        return JsonResponse({"message" : "NOT_EXISTS_ID"}, status=400)
    #인증 이메일 전송
    def email_Check(self, request, target_code=''):
        serializer_class = MemberSerializer
        try:
            
            if Member.objects.filter(id = target_code).exists():

                #전처리 한번 필요
                token = email_auth_num()
                message = f"인증번호는 {token} 입니다."
                mail_title = "mimi 이메일 인증 메일입니다."
                email = EmailMessage(mail_title, message, to=[target_code])
                email.send()
                return JsonResponse({"message" : token},status=200)
            return JsonResponse({"message" : "NOT_EXISTS_ID"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"},status=400)
    #패스워드 변경
    def change_Pw(self, request, id='', password=''):
        serializer_class = ChangeMemberPasswordSerializer
        
        try:

            if Member.objects.filter(id = id).exists():
                user = Member.objects.get(id=id)
                password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
                user.password = password
                user.save()
                return HttpResponse(status=200)
            return JsonResponse({"message" : "NOT_EXISTS_ID"},status=400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"},status=400)
        

#회원가입, 이메일 중복여부
class MemberView(viewsets.GenericViewSet, View):
    #Swagger 설명을 위해 필요
    serializer_class = MemberSerializer

    #회원가입
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Member.objects.filter(id = data["id"]).exists():
                return JsonResponse({"message" : "EXISTS_ID"}, status=400)
            #num 값 갱신
            user_email = data["id"]
            #전처리 한번 필요
            
            curr_max_num = Member.objects.all().count() + 949437
            print(curr_max_num)
            Member.objects.create(
                num = curr_max_num,
                id = data["id"],
                password = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                gender = data["gender"],
                birthday = data["birthday"]
            ).save()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"},status=400)
    #id중복여부 및 인증이메일 전송 api
    def get(self, request, target_code=''):
        try:

            if Member.objects.filter(id = target_code).exists():
                return JsonResponse({"message" : "EXISTS_ID"}, status=400)
            
            #전처리 한번 필요
            token = email_auth_num()
            message = f"인증번호는 {token} 입니다."
            mail_title = "mimi 이메일 인증 메일입니다."
            email = EmailMessage(mail_title, message, to=[target_code])
            email.send()
            return JsonResponse({"message" : token},status=200)
            

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"},status=400)
#로그인 클래스
class SignView(viewsets.GenericViewSet,View):
    serializer_class = MemberSerializer
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(id = data["id"]).exists():
                user = Member.objects.get(id = data["id"])
                #로그인 성공
                if bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")):
                    num = str(user.num)
                    
                    token = jwt.encode({"user" : num}, SECRET_KEY, algorithm="HS256")
                    
                    return JsonResponse({"token" : token},status=200)
                #실패
                return HttpResponse(status=401)
            return HttpResponse(status=401)# 400으로 적힘 두개 차이점 알기
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status=400)


        