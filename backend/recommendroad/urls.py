from django.urls import path
from django.conf import settings
from .views import RecommendTravle, UserInfo, Recommend
#from .views import *

urlpatterns = [

    path("recommend-travle", RecommendTravle.as_view({"post": "user_option"})),
    path("save-option-land", RecommendTravle.as_view({"post": "save_option_land"})),
    path("save-option-store", RecommendTravle.as_view({"post": "save_option_store"})),
    path("get-store-info/<str:sid>", UserInfo.as_view({"get": "get_store"})),
    path("get-user-schedule/<str:num>", UserInfo.as_view({"get": "get_user_schedule"})),
    path("get-user-schedule-detail/<str:num>,<str:date>", UserInfo.as_view({"get": "get_user_schedule_detail"})),
    path("road-sort", RecommendTravle.as_view({"post": "road_sort"})),
    path("hot-keyword-15", RecommendTravle.as_view({"post": "hot_keyword_15"})),
    path("keyword-storelist", RecommendTravle.as_view({"post": "keyword_storelist"})),
    path("post-review", RecommendTravle.as_view({"post": "post_review"})),
    path("get-all-review/<str:sid>", RecommendTravle.as_view({"get": "get_all_review"})),
    path("get-store-locate/<str:sid>", RecommendTravle.as_view({"get": "get_store_locate"})),
    path("land-distance-return", RecommendTravle.as_view({"post": "land_distance_return"})),
    path("distance-recommend", Recommend.as_view({"post": "distance_recommend"})),
    path("bigdata-recommend", Recommend.as_view({"post": "bigdata_recommend"})),
    path("star-recommend", Recommend.as_view({"post": "star_recommend"})),
    path("reviews-sum", Recommend.as_view({"post": "reviews_sum"})),
    path("main-storelist", RecommendTravle.as_view({"post": "main_storelist"})),
    
    
]
    
