from .models import Member, Store, Review, Menu, Landmark, ZzimStore, ZzimStoreCourse, ZzimLandCourse
from rest_framework import serializers

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
            # "sid",
            # "store_name",
            # "branch",
            # "area",
            # "tel",
            # "address",
            # "latitude",
            # "longitude",
            # "reviewCnt",
            # "category_list",
            # #"image",
    


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "rid",  
            "sid",  
            "num",  
            "score", 
            "content",  
            "reg_time", 
        )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "mid",  
            "store",  
            "menu_name",  
            "price"  
        ]

class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = [
            "lid",  
            "landmark_name",  
            "addr",  
            "latitude",
            "longitude",
            "facility",
            "parking",
            "desc",
            "tel",
            "theme"  
        ]

class ZzimStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZzimStore
        fields = [
            "num",  
            "sid" 
        ]

class ZzimStoreCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZzimStoreCourse
        fields = [
            "num",  
            "sidB",
            "isVisitedB",
            "sidL",
            "isVisitedL",
            "sidD",
            "isVisitedD", 
        ]   

class ZzimLandCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZzimLandCourse
        fields = [
            "num",
            "lid1",
            "lid2",
            "lid3",
            "lid4",
            "isSaved",
            "savedDate"
        ]

class UserOptionSerializer(serializers.Serializer):
    user_date = serializers.DateField(help_text="여행일자")
    user_location = serializers.IntegerField(help_text="선호지역")
    user_thema = serializers.CharField(help_text="선호테마")

class SaveOptionStoreSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="이메일")
    savedDate = serializers.CharField(help_text="해당일자")
    sid = serializers.CharField(help_text="음식점 번호")
    flag = serializers.IntegerField(help_text="0: 아침, 1: 점심, 2: 저녁")

class SaveOptionLandSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="이메일")
    lid1 = serializers.CharField(help_text="경로1")
    lid2 = serializers.CharField(help_text="경로2")
    lid3 = serializers.CharField(help_text="경로3")
    lid4 = serializers.CharField(help_text="경로4")
    savedDate = serializers.CharField(help_text="해당일자")

class ShortPathRoadSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="이메일")
    lid1 = serializers.CharField(help_text="경로1")
    lid2 = serializers.CharField(help_text="경로2")
    lid3 = serializers.CharField(help_text="경로3")
    lid4 = serializers.CharField(help_text="경로4")

class LatLogSerializer(serializers.Serializer):
    latitude = serializers.FloatField(help_text="위도")
    logitude = serializers.FloatField(help_text="경도")

class KeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField(help_text="키워드")
    latitude = serializers.FloatField(help_text="위도")
    logitude = serializers.FloatField(help_text="경도")

class ReviewNewSerializer(serializers.Serializer):
    num = serializers.CharField(help_text="유저 num")
    sid = serializers.CharField(help_text="가게 id")
    total_score = serializers.CharField(help_text="리뷰점수")
    content = serializers.CharField(help_text="댓글내용")
    flag = serializers.CharField(help_text="이전작성여부")
    predate = serializers.CharField(help_text="이전작성날짜")
    review_type = serializers.CharField(help_text="아침 : 0, 점심 : 1, 저녁 : 2")
    review_id = serializers.CharField(help_text="음식점 저장 id")

class LandDistanceReturnSerializer(serializers.Serializer):
    num = serializers.CharField(help_text="유저 num")
    lid1 = serializers.CharField(help_text="경로1")
    lid2 = serializers.CharField(help_text="경로2")
    lid3 = serializers.CharField(help_text="경로3")
    lid4 = serializers.CharField(help_text="경로4")

class RecommendStoreSerializer(serializers.Serializer):
    u_address = serializers.CharField(help_text="2번째 주소")
    u_lat = serializers.CharField(help_text="위도")
    u_long = serializers.CharField(help_text="경도")

class RecommendStarSerializer(serializers.Serializer):
    u_address = serializers.CharField(help_text="2번째 주소")
    u_lat = serializers.CharField(help_text="위도")
    u_long = serializers.CharField(help_text="경도")
class RecommendBigdataSerializer(serializers.Serializer):
    u_address = serializers.CharField(help_text="2번째 주소")
    u_lat = serializers.CharField(help_text="위도")
    u_long = serializers.CharField(help_text="경도")
    num = serializers.CharField(help_text="user num")