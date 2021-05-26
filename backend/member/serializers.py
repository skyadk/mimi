from .models import Member
from rest_framework import serializers

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.EmailField(help_text="email형식") #email형식
    password = serializers.CharField(help_text="비밀번호")
    gender = serializers.BooleanField(help_text="성별 0 : 남자, 1: 여자")
    birthday = serializers.DateField(help_text="생년월일")
    class Meta:
        member = Member.objects.all()
        model = Member
        #'__all__' 사용시 모든 필드
        fields = ("id", "password", "gender", "birthday")

class ChangeMemberPasswordSerializer(serializers.Serializer):
    id = serializers.EmailField(help_text="변경할 이메일")
    password = serializers.CharField(help_text="비밀번호")
    class Meta:
        member = Member.objects.all()
        model = Member
        fields = ("id", "password")

class SearchMemberIdSerializer(serializers.Serializer):
    id = serializers.EmailField(help_text="변경할 이메일")
    birthday = serializers.DateField(help_text="생년월일")
    class Meta:
        member = Member.objects.all()
        model = Member
        fields = ("id", "birthday")