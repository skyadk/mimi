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
    user_date = serializers.DateField(help_text="????????????")
    user_location = serializers.IntegerField(help_text="????????????")
    user_thema = serializers.CharField(help_text="????????????")

class SaveOptionStoreSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="?????????")
    savedDate = serializers.CharField(help_text="????????????")
    sid = serializers.CharField(help_text="????????? ??????")
    flag = serializers.IntegerField(help_text="0: ??????, 1: ??????, 2: ??????")

class SaveOptionLandSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="?????????")
    lid1 = serializers.CharField(help_text="??????1")
    lid2 = serializers.CharField(help_text="??????2")
    lid3 = serializers.CharField(help_text="??????3")
    lid4 = serializers.CharField(help_text="??????4")
    savedDate = serializers.CharField(help_text="????????????")

class ShortPathRoadSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="?????????")
    lid1 = serializers.CharField(help_text="??????1")
    lid2 = serializers.CharField(help_text="??????2")
    lid3 = serializers.CharField(help_text="??????3")
    lid4 = serializers.CharField(help_text="??????4")

class LatLogSerializer(serializers.Serializer):
    latitude = serializers.FloatField(help_text="??????")
    logitude = serializers.FloatField(help_text="??????")

class KeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField(help_text="?????????")
    latitude = serializers.FloatField(help_text="??????")
    logitude = serializers.FloatField(help_text="??????")

class ReviewNewSerializer(serializers.Serializer):
    num = serializers.CharField(help_text="?????? num")
    sid = serializers.CharField(help_text="?????? id")
    total_score = serializers.CharField(help_text="????????????")
    content = serializers.CharField(help_text="????????????")
    flag = serializers.CharField(help_text="??????????????????")
    predate = serializers.CharField(help_text="??????????????????")
    review_type = serializers.CharField(help_text="?????? : 0, ?????? : 1, ?????? : 2")
    review_id = serializers.CharField(help_text="????????? ?????? id")

class LandDistanceReturnSerializer(serializers.Serializer):
    num = serializers.CharField(help_text="?????? num")
    lid1 = serializers.CharField(help_text="??????1")
    lid2 = serializers.CharField(help_text="??????2")
    lid3 = serializers.CharField(help_text="??????3")
    lid4 = serializers.CharField(help_text="??????4")

class RecommendStoreSerializer(serializers.Serializer):
    u_address = serializers.CharField(help_text="2?????? ??????")
    u_lat = serializers.CharField(help_text="??????")
    u_long = serializers.CharField(help_text="??????")

class RecommendStarSerializer(serializers.Serializer):
    u_address = serializers.CharField(help_text="2?????? ??????")
    u_lat = serializers.CharField(help_text="??????")
    u_long = serializers.CharField(help_text="??????")
class RecommendBigdataSerializer(serializers.Serializer):
    u_address = serializers.CharField(help_text="2?????? ??????")
    u_lat = serializers.CharField(help_text="??????")
    u_long = serializers.CharField(help_text="??????")
    num = serializers.CharField(help_text="user num")