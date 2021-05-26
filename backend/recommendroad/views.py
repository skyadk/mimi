from django.shortcuts import render
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from django.http import Http404, HttpResponse, JsonResponse
from .models import Landmark, ZzimStoreCourse, ZzimLandCourse, Store, Menu, RScoreTable, Review, BigdataCount, BigdataProcess
from member.models import Member
from backend.settings import T_KEY
from .serializers import StoreSerializer,UserOptionSerializer, SaveOptionStoreSerializer, SaveOptionLandSerializer, ShortPathRoadSerializer, ReviewNewSerializer, LandDistanceReturnSerializer, LatLogSerializer, KeywordSerializer, RecommendStoreSerializer, RecommendStarSerializer, RecommendBigdataSerializer
from django.db.models import Max 
from django.core import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from haversine import haversine
from datetime import datetime
from django.utils.dateformat import DateFormat
import pandas as pd
import urllib.request
import json
import bcrypt
import jwt
import requests
import random
import copy
from django.db.models import Q
import sqlalchemy

class UserInfo(viewsets.GenericViewSet, View):
    # 저장 정보 전달(아침점심저녁 간단정보)
    def get_user_schedule(self, request, num=''):
        if Member.objects.filter(num = num).exists() :
            #예약 음식 가져오기
            zzimlist = ZzimStoreCourse.objects.filter(num = num)
            result_set = []

            for row in zzimlist.values_list() :
                sb_name = "NULL" 
                sl_name = "NULL"
                sd_name = "NULL"
                
                if row[2] != None :
                    sb = Store.objects.get(sid = row[2])
                    sb_name = sb.store_name
                if row[4] != None :
                    sl = Store.objects.get(sid = row[4])
                    sl_name = sl.store_name
                if row[6] != None :     
                    sd = Store.objects.get(sid = row[6])
                    sd_name = sd.store_name
                add_set = { 
                            "id" : row[0],
                            "sidB" : row[2],
                            "isSavedB" : row[3],
                            "sidBName" : sb_name,
                            "sidL" : row[4],
                            "isSavedL" : row[5],
                            "sidLName" : sl_name,
                            "sidD" : row[6],
                            "isSavedD" : row[7],
                            "sidDName" : sd_name,
                            "savedDate" : row[8]
                            }
                
                result_set.append(add_set)
            return JsonResponse({"message" : result_set}, status=200)


        return JsonResponse({"message" : "err"}, status=400)
    #저장정보 전달(디테일)
    def get_user_schedule_detail(self, request, num='', date=''):
        print(num)
        if Member.objects.filter(num = num).exists():
            #당일 예약은 1개
            
            zzimlist = ZzimStoreCourse.objects.filter(num = num, savedDate=date)
            zzimlandlist = ZzimLandCourse.objects.filter(num = num, savedDate=date)
            print(zzimlist[0].sidB)
            print(len(zzimlandlist))
            result_store = []
            result_land = []
            #수정
            #아침
            if len(zzimlist) > 0 :
                if Store.objects.filter(sid=zzimlist[0].sidB).exists():
                    store = Store.objects.get(sid=zzimlist[0].sidB)
                    store_set = { "sidB" : store.sid,
                                    "store_name" : store.store_name,
                                    "branch" : store.branch,
                                    "area" : store.area,
                                    "tel" : store.tel,
                                    "address" : store.address,
                                    "latitude" : store.latitude,
                                    "logitude" : store.logitude,
                                    "review_cnt" : store.review_cnt,
                                    "category" : store.category,
                                    "isSavedB" : zzimlist[0].isSavedB
                    }
                else : 
                    store_set = { "sidB" : "NULL"}
                result_store.append(store_set)
                #점심
                if Store.objects.filter(sid=zzimlist[0].sidL).exists():
                    store = Store.objects.get(sid=zzimlist[0].sidL)
                    store_set = { "sidL" : store.sid,
                                    "store_name" : store.store_name,
                                    "branch" : store.branch,
                                    "area" : store.area,
                                    "tel" : store.tel,
                                    "address" : store.address,
                                    "latitude" : store.latitude,
                                    "logitude" : store.logitude,
                                    "review_cnt" : store.review_cnt,
                                    "category" : store.category,
                                    "isSavedL" : zzimlist[0].isSavedL
                    }
                else :
                    store_set = { "sidL" : "NULL"}    
                result_store.append(store_set)
                #저녁
                if Store.objects.filter(sid=zzimlist[0].sidD).exists():
                    store = Store.objects.get(sid=zzimlist[0].sidD)
                    store_set = { "sidD" : store.sid,
                                    "store_name" : store.store_name,
                                    "branch" : store.branch,
                                    "area" : store.area,
                                    "tel" : store.tel,
                                    "address" : store.address,
                                    "latitude" : store.latitude,
                                    "logitude" : store.logitude,
                                    "review_cnt" : store.review_cnt,
                                    "category" : store.category,
                                    "isSavedD" : zzimlist[0].isSavedD
                    }
                else :
                    store_set = { "sidD" : "NULL"}
                result_store.append(store_set)
            else :
                store_set = { "sidB" : "NULL"}
                result_store.append(store_set)
                store_set = { "sidL" : "NULL"}
                result_store.append(store_set)
                store_set = { "sidD" : "NULL"}
                result_store.append(store_set)
            if len(zzimlandlist) > 0 :
              
                if Landmark.objects.filter(lid = zzimlandlist[0].lid1).exists() :
                  
                    land = Landmark.objects.get(lid = zzimlandlist[0].lid1)
               
                    add_set = { "lid" : land.lid,
                                "landmark_name" : land.landmark_name,
                                "addr" : land.addr,
                                "latitude" : land.latitude,
                                "longitude" : land.logitude,
                                "facility" : land.facility,
                                "park" : land.park,
                                "desc" : land.desc,
                                "tel" : land.tel,
                                "theme" : land.theme
                                }
                else :
                    add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                if Landmark.objects.filter(lid = zzimlandlist[0].lid2).exists() :
                    land = Landmark.objects.get(lid = zzimlandlist[0].lid2)
                    add_set = { "lid" : land.lid,
                                "landmark_name" : land.landmark_name,
                                "addr" : land.addr,
                                "latitude" : land.latitude,
                                "longitude" : land.logitude,
                                "facility" : land.facility,
                                "park" : land.park,
                                "desc" : land.desc,
                                "tel" : land.tel,
                                "theme" : land.theme
                                }
                else :
                    add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                if Landmark.objects.filter(lid = zzimlandlist[0].lid3).exists() :
                    land = Landmark.objects.get(lid = zzimlandlist[0].lid3)
                    add_set = { "lid" : land.lid,
                                "landmark_name" : land.landmark_name,
                                "addr" : land.addr,
                                "latitude" : land.latitude,
                                "longitude" : land.logitude,
                                "facility" : land.facility,
                                "park" : land.park,
                                "desc" : land.desc,
                                "tel" : land.tel,
                                "theme" : land.theme
                                }
                else :
                    add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                if Landmark.objects.filter(lid = zzimlandlist[0].lid4).exists() :
                    land = Landmark.objects.get(lid = zzimlandlist[0].lid4)
                    add_set = { "lid" : land.lid,
                                "landmark_name" : land.landmark_name,
                                "addr" : land.addr,
                                "latitude" : land.latitude,
                                "longitude" : land.logitude,
                                "facility" : land.facility,
                                "park" : land.park,
                                "desc" : land.desc,
                                "tel" : land.tel,
                                "theme" : land.theme
                                }
                else :
                    add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                distance = []
                #1to2
                if (zzimlandlist[0].lid2 !="NULL") :
                    land1 = Landmark.objects.get(lid = zzimlandlist[0].lid1)
                    land2 = Landmark.objects.get(lid = zzimlandlist[0].lid2)
                    data = {
                        "startX" : land1.logitude,
                        "startY" : land1.latitude,
                        "endX" : land2.logitude,
                        "endY" : land2.latitude,
                        "reqCoordType" : "WGS84GEO",
                        "resCchOption" : "0",
                        "trafficInfo" : "N"
                    }
                    data = json.dumps(data)
                    randomkey = random.randint(0,len(T_KEY)-1)
                    headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
                    url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
                    res = requests.post(url, data=data, headers=headers)
                    json_object = res.json()
                    totalDistance = json_object["features"][0]["properties"]["totalDistance"]
                    totalDistance = totalDistance/1000
                    totalDistance = round(totalDistance,1)
                    add_set = {"one_two" : totalDistance}
                else :
                    add_set = {"one_two" : "NULL"}
                distance.append(add_set)
                #2to3
                if (zzimlandlist[0].lid3 !="NULL") :
                    land1 = Landmark.objects.get(lid = zzimlandlist[0].lid2)
                    land2 = Landmark.objects.get(lid = zzimlandlist[0].lid3)
                    data = {
                        "startX" : land1.logitude,
                        "startY" : land1.latitude,
                        "endX" : land2.logitude,
                        "endY" : land2.latitude,
                        "reqCoordType" : "WGS84GEO",
                        "resCchOption" : "0",
                        "trafficInfo" : "N"
                    }
                    data = json.dumps(data)
                    randomkey = random.randint(0,len(T_KEY)-1)
                    headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
                    url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
                    res = requests.post(url, data=data, headers=headers)
                    json_object = res.json()
                    totalDistance = json_object["features"][0]["properties"]["totalDistance"]
                    totalDistance = totalDistance/1000
                    totalDistance = round(totalDistance,1)
                    add_set = {"two_three" : totalDistance}
                else :
                    add_set = {"two_three" : "NULL"}
                distance.append(add_set)
                #3to4
                if (zzimlandlist[0].lid4 !="NULL") :
                    land1 = Landmark.objects.get(lid = zzimlandlist[0].lid3)
                    land2 = Landmark.objects.get(lid = zzimlandlist[0].lid4)
                    data = {
                        "startX" : land1.logitude,
                        "startY" : land1.latitude,
                        "endX" : land2.logitude,
                        "endY" : land2.latitude,
                        "reqCoordType" : "WGS84GEO",
                        "resCchOption" : "0",
                        "trafficInfo" : "N"
                    }
                    data = json.dumps(data)
                    randomkey = random.randint(0,len(T_KEY)-1)
                    headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
                    url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
                    res = requests.post(url, data=data, headers=headers)
                    json_object = res.json()
                    totalDistance = json_object["features"][0]["properties"]["totalDistance"]
                    totalDistance = totalDistance/1000
                    totalDistance = round(totalDistance,1)
                    add_set = {"three_four" : totalDistance}
                else :
                    add_set = {"three_four" : "NULL"}
                distance.append(add_set)
                return JsonResponse({"store_info" : result_store, "land_info" : result_land, "distance" : distance}, status=200)
            else :
                add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                add_set = { "lid" : "NULL"}
                result_land.append(add_set)
                distance = []
                add_set = {"one_two" : "NULL"}
                distance.append(add_set)
                add_set = {"two_three" : "NULL"}
                distance.append(add_set)
                add_set = {"three_four" : "NULL"}
                distance.append(add_set)
            return JsonResponse({"store_info" : result_store, "land_info" : result_land, "distance" : distance}, status=200) 
        return JsonResponse({"message" : "err"}, status=400)

    

    # 음식점 정보 전달
    def get_store(self, request, sid='') :
        
        if Store.objects.filter(sid = sid).exists():
            print(sid)
            result_set = []
            #음식점 정보 가져오기
            store = Store.objects.get(sid=sid)
            reviews = Review.objects.filter(sid = sid)
            review_score = 0
            
            if len(reviews) !=0 :
                sum_score = 0
                for row in reviews.values_list() :
                    sum_score = sum_score + int(row[3])
                sum_score = sum_score/len(reviews)
                review_score = round(sum_score,1)

            store_set = { "sid" : store.sid,
                            "store_name" : store.store_name,
                            "branch" : store.branch,
                            "area" : store.area,
                            "tel" : store.tel,
                            "address" : store.address,
                            "latitude" : store.latitude,
                            "logitude" : store.logitude,
                            "review_cnt" : store.review_cnt,
                            "category" : store.category,
                            "review_score" : review_score
                            }
            result_set.append(store_set)
            #메뉴 정보 가져오기
            
            if Menu.objects.filter(sid=sid).exists():
                
                menus = Menu.objects.filter(sid=sid)
                menu_info = []
                
                for row in menus.values_list() :
                    
                    add_set = { "mid" : row[0],
                            "sid" : row[1],
                            "menu_name" : row[2],
                            "price" : row[3]
                            
                            }
                    menu_info.append(add_set)
                result_set.append(menu_info)
                return JsonResponse({"message" : result_set}, status=200)
            #메뉴 정보가 없으면
            else :
                
                menu_info = {"mid" : "NULL"}
                result_set.append(menu_info)
                return JsonResponse({"message" : result_set}, status=200)
            
            
        return JsonResponse({"message" : "err"}, status=400)



class Recommend(viewsets.GenericViewSet, View):
    # def reviews_sum(self,request) :
    #     stores = Store.objects.filter(review_cnt__gt=0)
    #     print(len(stores))
    #     for row in stores.values_list() :
    #         change = Store.objects.get(sid = row[0])

    #         reviews = Review.objects.filter(sid = row[0]).only("total_score")
    #         score = 0
    #         for row1 in reviews.values_list() :
    #             score = int(score) + int(row1[3])
    #         if len(reviews) != 0 :
    #             score = score/len(reviews)
    #             score = round(score,1)
    #         change.review_sum = score
    #         change.save()

#별점기반 추천
    @swagger_auto_schema(request_body = RecommendStarSerializer)
    def star_recommend(self, request):
        data = json.loads(request.body)
        stores = Store.objects.filter(address__contains = data["u_address"],review_cnt__gt=0).values_list()
        
        result_set = []
        curr_set = []
        if len(stores) ==0 :
            add_set = {
                "sid" : "NULL"
            }
            result_set.append(add_set)
        else :
            curr_set = sorted(stores, key=lambda stores: stores[11], reverse=True)

            su = 0
            for row in curr_set :
                print(row)
                if su == 50 :
                    break
                curr = (float(data["u_lat"]), float(data["u_long"])) #Latitude, Longitude
                arrive = (float(row[6]), float(row[7])) 
                # 거리 계산 
                km = haversine(curr, arrive, unit = 'km')
                km = round(km,2)
                if km>10 :
                    continue
                
                add_set = {
                    "sid" : row[0],
                    "store_name" : row[1],
                    "branch" : row[2],
                    "area" : row[3],
                    "tel" : row[4],
                    "address" : row[5],
                    "latitude" : row[6],
                    "logitude" : row[7],
                    "review_cnt" : row[8],
                    "category" : row[10],
                    "review_avg" : row[11],
                    "km" : km
                }
                result_set.append(add_set)
                su+=1

        return JsonResponse({"message" : result_set}, status=200) 
    #거리순으로 50개 리턴 위도, 경도, 경로
    @swagger_auto_schema(request_body = RecommendStoreSerializer)
    def distance_recommend(self, request):
        data = json.loads(request.body)
        stores = Store.objects.filter(address__contains = data["u_address"])
        result_set = []
        curr_set = []
        randomkey = random.randint(0,len(T_KEY)-1)
        
        if len(stores) ==0 :
            add_set = {
                "sid" : "NULL"
            }
            result_set.append(add_set)
        else :
            for row in stores.values_list() :
                
                curr = (float(data["u_lat"]), float(data["u_long"])) #Latitude, Longitude
                arrive = (float(row[6]), float(row[7])) 
                # 거리 계산 
                km = haversine(curr, arrive, unit = 'km')
                km = round(km,2)
                
                add_set = {
                    "sid" : row[0],
                    "store_name" : row[1],
                    "branch" : row[2],
                    "area" : row[3],
                    "tel" : row[4],
                    "address" : row[5],
                    "latitude" : row[6],
                    "logitude" : row[7],
                    "review_cnt" : row[8],
                    "category" : row[10],
                    "review_avg" : row[11],
                    "km" : km
                }
                curr_set.append(add_set)
            curr_set = sorted(curr_set, key=lambda curr_set: curr_set["km"])
            for i in range(len(curr_set)):
                if i == 50 :
                    break
                else :
                    result_set.append(curr_set[i])
        return JsonResponse({"message" : result_set}, status=200) 
    
    
    
    #빅데이터 분석으로 리턴
    @swagger_auto_schema(request_body = RecommendBigdataSerializer)
    def bigdata_recommend(self, request):
        data = json.loads(request.body)
        stores = Store.objects.filter(address__contains = data["u_address"])
        result_set = []
        if len(stores) ==0 :
            add_set = {
                "sid" : "NULL"
            }
            result_set.append(add_set)
        else :
            # 리뷰남긴게 있는지
            if BigdataProcess.objects.filter(num = data["num"]).exists():
                process = BigdataProcess.objects.get(num = data["num"])
                print(process.num)
                # 다른 리뷰가 잇는지
                if BigdataProcess.objects.exclude(num = data["num"]).exists():
                    other = BigdataProcess.objects.exclude(num = data["num"])
                    first_result = []
                    for row in other.values_list() :
                        # 절대값을 구해서 리스트에 추가
                        print(row)
                        abs_sum = abs(process.jandt - row[1]) + abs(process.candd - row[2]) + abs(process.chfood - row[3]) + abs(process.chicken - row[4]) + abs(process.pizza - row[5]) + abs(process.fastfood - row[6]) + abs(process.bunfood - row[7]) + abs(process.jpfood - row[8]) + abs(process.krfood - row[9]) + abs(process.jandb - row[10]) + abs(process.aanda - row[11]) + abs(process.etc - row[12])
                        add_set = {
                            "num" : row[0],
                            "abs_sum" : abs_sum
                        }
                        first_result.append(add_set)
                    #결과값을 오름차순 정렬
                    first_result = sorted(first_result, key=lambda first_result: first_result["abs_sum"])
                    rst_num = first_result[0]["num"]
                    reviews = Review.objects.filter(num = rst_num, total_score__gte = 3).values("sid").distinct()
                    pre = 0
                    for row in reviews.values_list() :
                        if pre == row[1] :
                            continue
                        pre = row[1]
                        store = Store.objects.get(sid = row[1])
                        curr = (float(data["u_lat"]), float(data["u_long"])) #Latitude, Longitude
                        arrive = (float(store.latitude), float(store.logitude)) 
                        # 거리 계산 
                        km = haversine(curr, arrive, unit = 'km')
                        km = round(km,2)
                        if km > 15 :
                            continue
                        if store.review_avg <3 :
                            continue
                        add_set = {
                            "sid" : store.sid,
                            "store_name" : store.store_name,
                            "branch" : store.branch,
                            "area" : store.area,
                            "tel" : store.tel,
                            "address" : store.address,
                            "latitude" : store.latitude,
                            "logitude" : store.logitude,
                            "review_cnt" : store.review_cnt,
                            "category" : store.category,
                            "review_avg" : store.review_avg,
                            "km" : km
                        }
                        result_set.append(add_set)
                    if len(result_set) < 1 :
                        add_set = {
                        "sid" : "NULL"
                        }
                        result_set.append(add_set)
                else :
                    add_set = {
                    "sid" : "NULL"
                    }
                    result_set.append(add_set)
            else :
                add_set = {
                "sid" : "NULL"
                }
                result_set.append(add_set)



        return JsonResponse({"message" : result_set}, status=200) 


class RecommendTravle(viewsets.GenericViewSet, View):
    



    #lid 받아서 lid안에 정보 및 거리 계산 후 리턴
    @swagger_auto_schema(request_body = LandDistanceReturnSerializer)
    def land_distance_return(self,request) :
        udata = json.loads(request.body)
        

        if Member.objects.filter(num = udata["num"]).exists():
            result_land = []
            if Landmark.objects.filter(lid = udata["lid1"]).exists() :
                land = Landmark.objects.get(lid = udata["lid1"])
                add_set = { "lid1" : land.lid,
                            "landmark_name" : land.landmark_name,
                            "addr" : land.addr,
                            "latitude" : land.latitude,
                            "longitude" : land.logitude,
                            "facility" : land.facility,
                            "park" : land.park,
                            "desc" : land.desc,
                            "tel" : land.tel,
                            "theme" : land.theme
                            }
            else :
                add_set = { "lid1" : "NULL"}
            result_land.append(add_set)
            if Landmark.objects.filter(lid = udata["lid2"]).exists() :
                land = Landmark.objects.get(lid = udata["lid2"])
                add_set = { "lid2" : land.lid,
                            "landmark_name" : land.landmark_name,
                            "addr" : land.addr,
                            "latitude" : land.latitude,
                            "longitude" : land.logitude,
                            "facility" : land.facility,
                            "park" : land.park,
                            "desc" : land.desc,
                            "tel" : land.tel,
                            "theme" : land.theme
                            }
            else :
                add_set = { "lid2" : "NULL"}
            result_land.append(add_set)
            if Landmark.objects.filter(lid = udata["lid3"]).exists() :
                land = Landmark.objects.get(lid = udata["lid3"])
                add_set = { "lid3" : land.lid,
                            "landmark_name" : land.landmark_name,
                            "addr" : land.addr,
                            "latitude" : land.latitude,
                            "longitude" : land.logitude,
                            "facility" : land.facility,
                            "park" : land.park,
                            "desc" : land.desc,
                            "tel" : land.tel,
                            "theme" : land.theme
                            }
            else :
                add_set = { "lid3" : "NULL"}
            result_land.append(add_set)
            if Landmark.objects.filter(lid = udata["lid4"]).exists() :
                land = Landmark.objects.get(lid = udata["lid4"])
                add_set = { "lid4" : land.lid,
                            "landmark_name" : land.landmark_name,
                            "addr" : land.addr,
                            "latitude" : land.latitude,
                            "longitude" : land.logitude,
                            "facility" : land.facility,
                            "park" : land.park,
                            "desc" : land.desc,
                            "tel" : land.tel,
                            "theme" : land.theme
                            }
            else :
                add_set = { "lid4" : "NULL"}
            result_land.append(add_set)
            
            distance = []
            sumDistance = 0     
            #1to2
            if (udata["lid2"] != "NULL") :
                land1 = Landmark.objects.get(lid = udata["lid1"])
                land2 = Landmark.objects.get(lid = udata["lid2"])
                data = {
                    "startX" : land1.logitude,
                    "startY" : land1.latitude,
                    "endX" : land2.logitude,
                    "endY" : land2.latitude,
                    "reqCoordType" : "WGS84GEO",
                    "resCchOption" : "0",
                    "trafficInfo" : "N"
                }
                data = json.dumps(data)
                randomkey = random.randint(0,len(T_KEY)-1)
                headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
                url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
                res = requests.post(url, data=data, headers=headers)
                json_object = res.json()
                totalDistance = json_object["features"][0]["properties"]["totalDistance"]
                totalDistance = totalDistance/1000
                totalDistance = round(totalDistance,1)
                sumDistance = sumDistance + totalDistance
                add_set = {"one_two" : totalDistance}
            else :
                add_set = {"one_two" : "NULL"}
            distance.append(add_set)
  
            #2to3
            
            
            if (udata["lid3"] != "NULL") :
                land1 = Landmark.objects.get(lid = udata["lid2"])
                land2 = Landmark.objects.get(lid = udata["lid3"])
                data = {
                    "startX" : land1.logitude,
                    "startY" : land1.latitude,
                    "endX" : land2.logitude,
                    "endY" : land2.latitude,
                    "reqCoordType" : "WGS84GEO",
                    "resCchOption" : "0",
                    "trafficInfo" : "N"
                }
                data = json.dumps(data)
                randomkey = random.randint(0,len(T_KEY)-1)
                headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
                url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
                res = requests.post(url, data=data, headers=headers)
                json_object = res.json()
                totalDistance = json_object["features"][0]["properties"]["totalDistance"]
                totalDistance = totalDistance/1000
                totalDistance = round(totalDistance,1)
                add_set = {"two_three" : totalDistance}
                sumDistance = sumDistance + totalDistance
            else :
                add_set = {"two_three" : "NULL"}
            distance.append(add_set)
            #3to4
            if udata["lid4"] !="NULL" :
                land1 = Landmark.objects.get(lid = udata["lid3"])
                land2 = Landmark.objects.get(lid = udata["lid4"])
                data = {
                    "startX" : land1.logitude,
                    "startY" : land1.latitude,
                    "endX" : land2.logitude,
                    "endY" : land2.latitude,
                    "reqCoordType" : "WGS84GEO",
                    "resCchOption" : "0",
                    "trafficInfo" : "N"
                }
                data = json.dumps(data)
                randomkey = random.randint(0,len(T_KEY)-1)
                headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
                url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
                res = requests.post(url, data=data, headers=headers)
                json_object = res.json()
                totalDistance = json_object["features"][0]["properties"]["totalDistance"]
                totalDistance = totalDistance/1000
                totalDistance = round(totalDistance,1)
                sumDistance = sumDistance + totalDistance
                add_set = {"three_four" : totalDistance}
                
            else :
                add_set = {"three_four" : "NULL"}
            distance.append(add_set)
            return JsonResponse({"land_info" : result_land, "distance" : distance, "totalDistance" : sumDistance}, status=200)
        return JsonResponse({"message" : "err"}, status=400) 

    #가게 위치정보 리턴
    def get_store_locate(self, request, sid='') :
        if Store.objects.filter(sid = sid) :
            result_set = []
            store = Store.objects.get(sid = sid)
            store_set = { "sidB" : store.sid,
                                    "store_name" : store.store_name,
                                    "branch" : store.branch,
                                    "area" : store.area,
                                    "tel" : store.tel,
                                    "address" : store.address,
                                    "latitude" : store.latitude,
                                    "logitude" : store.logitude,
                                    "review_cnt" : store.review_cnt,
                                    "category" : store.category
                    }
            result_set.append(store_set)
            return JsonResponse({"result_set" : result_set}, status=200) 
        return JsonResponse({"result_set" : "NULL"}, status=200) 
    #해당 가게 전체리뷰 조회
    def get_all_review(self, request, sid='') :
        if Review.objects.filter(sid = sid).exists() :
            result_set = []
            reviews = Review.objects.filter(sid = sid)
            for row in reviews.values_list() :
                add_set = {
                            "rid" : row[0],
                            "sid" : row[1],
                            "num" : row[2],
                            "total_score" : row[3],
                            "content" : row[4],
                            "reg_time" : row[5]
                            
                        } 
                result_set.append(add_set)
            return JsonResponse({"result_set" : result_set}, status=200) 

        return JsonResponse({"result_set" : "NULL"}, status=200) 

    #리뷰 작성 
    @swagger_auto_schema(request_body = ReviewNewSerializer)
    def post_review(self,request) :
        data = json.loads(request.body)
        user_id = data["num"]
        #user_num, store_id, store_score, content, date
        
        if Member.objects.filter(num = data["num"]).exists():
            
            if Store.objects.filter(sid = data["sid"]).exists():
               
                if data["flag"] == "false" :
                    
                    dt_now = datetime.now()
                    
                    obj = Review.objects.count()
                    
                    Review.objects.create(
                        
                        #계산해야함
                        rid = int(obj)+10,
                        num = data["num"],
                        sid = data["sid"],
                        total_score = data["total_score"],
                        content = data["content"],
                        reg_time = dt_now.date()
                    )
                    # 리뷰계산
                    store = Store.objects.get(sid = data["sid"])
                    store.review_cnt = int(store.review_cnt)+1
                    # 평균계산
                    sum_score = 0
                    
                    score_all = Review.objects.filter(sid = data["sid"])
                    for row in score_all.values_list() :
                        sum_score = sum_score + int(row[3])
                    store.review_sum = sum_score
                    sum_score = sum_score/store.review_cnt
                    sum_score = round(sum_score,1)
                    store.review_avg = sum_score
                    category = store.category
                    store.save()
                    
                    # 방문여부 변경
                    #아침 0, 점심 1,저녁 2
                    if data["review_type"] == "0" :
                        zzim = ZzimStoreCourse.objects.get(id = data["review_id"])
                        zzim.isSavedB = "True"
                        zzim.save()
                    elif data["review_type"] == "1" :
                        zzim = ZzimStoreCourse.objects.get(id = data["review_id"])
                        zzim.isSavedL = "True"
                        zzim.save()
                    elif data["review_type"] == "2" :
                        zzim = ZzimStoreCourse.objects.get(id = data["review_id"])
                        zzim.isSavedD = "True"
                        zzim.save()
                    #빅데이터 리뷰카운터 작성
                    if BigdataCount.objects.filter(num = data["num"]).exists() :
                        if category == "찜/탕" :
                            data = BigdataCount.objects.get(num = data["num"])
                            data.jandt = data.jandt+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "중식" :
                            data = BigdataCount.objects.get(num = data["num"])
                            data.chfood = data.chfood+1
                            data.sumcount = data.sumcount+1
                            data.save()
                            
                        elif category == "치킨" :
                            data = BigdataCount.objects.get(num = data["num"])
                            data.chicken = data.chicken+1
                            data.sumcount = data.sumcount+1
                            data.save()
                            
                        elif category == "피자" :
                            data = BigdataCount.objects.get(num = data["num"])
                            data.pizza = data.pizza+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "패스트푸드" :
                            
                            # t
                            data = BigdataCount.objects.get(num = data["num"])
                            data.fastfood = data.fastfood+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "분식" :
                            
                            data = BigdataCount.objects.get(num = data["num"])
                            data.bunfood = data.bunfood+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "일식" :
                            
                            data = BigdataCount.objects.get(num = data["num"])
                            data.jpfood = data.jpfood+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "한식" :
                            
                            data = BigdataCount.objects.get(num = data["num"])
                            data.krfood = data.krfood+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "족발/보쌈" :
                            
                            data = BigdataCount.objects.get(num = data["num"])
                            data.jandb = data.jandb+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "아시안/양식" :
                            
                            data = BigdataCount.objects.get(num = data["num"])
                            data.aanda = data.aanda+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        elif category == "카페/디저트" :
                           
                            data = BigdataCount.objects.get(num = data["num"])
                            data.candd = data.candd+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        else :
                            
                            data = BigdataCount.objects.get(num = data["num"])
                            data.etc = data.etc+1
                            data.sumcount = data.sumcount+1
                            data.save()
                        
                    else :
                        # 생성
                        if category == "찜/탕" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            jandt = 1,
                            sumcount = 1)
                        elif category == "중식" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            chfood = 1,
                            sumcount = 1)
                        elif category == "치킨" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            chicken = 1,
                            sumcount = 1)
                        elif category == "피자" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            pizza = 1,
                            sumcount = 1)
                        elif category == "패스트푸드" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            fastfood = 1,
                            sumcount = 1)
                        elif category == "분식" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            bunfood = 1,
                            sumcount = 1)
                        elif category == "일식" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            jpfood = 1,
                            sumcount = 1)
                        elif category == "한식" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            krfood = 1,
                            sumcount = 1)
                        elif category == "족발/보쌈" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            jandb = 1,
                            sumcount = 1)
                        elif category == "아시안/양식" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            aanda = 1,
                            sumcount = 1)
                        elif category == "카페/디저트" :
                            BigdataCount.objects.create(
                            num = data["num"],
                            candd = 1,
                            sumcount = 1)
                        else :
                            BigdataCount.objects.create(
                            num = data["num"],
                            etc = 1,
                            sumcount = 1)
                        
                        
                    #빅데이터 리뷰 갱신
                    if BigdataProcess.objects.filter(num = int(user_id)).exists() :
                        bigdata = BigdataProcess.objects.get(num = int(user_id))
                        data = BigdataCount.objects.get(num = int(user_id))
                        sum = data.sumcount
                        curr = data.jandt/sum
                        bigdata.jandt = round(curr,3)
                        curr = data.candd/sum
                        bigdata.candd = round(curr,3)
                        curr = data.chfood/sum
                        bigdata.chfood = round(curr,3)
                        curr = data.chicken/sum
                        bigdata.chicken = round(curr,3)
                        curr = data.pizza/sum
                        bigdata.pizza = round(curr,3)
                        curr = data.fastfood/sum
                        bigdata.fastfood = round(curr,3)
                        curr = data.bunfood/sum
                        bigdata.bunfood = round(curr,3)
                        curr = data.jpfood/sum
                        bigdata.jpfood = round(curr,3)
                        curr = data.krfood/sum
                        bigdata.krfood = round(curr,3)
                        curr = data.jandb/sum
                        bigdata.jandb = round(curr,3)
                        curr = data.aanda/sum
                        bigdata.aanda = round(curr,3)
                        curr = data.etc/sum
                        bigdata.etc = round(curr,3)
                        bigdata.save()
                    else :
                        #생성
                        if category == "찜/탕" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            jandt = 1)
                        elif category == "중식" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            chfood = 1)
                        elif category == "치킨" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            chicken = 1)
                        elif category == "피자" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            pizza = 1)
                        elif category == "패스트푸드" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            fastfood = 1)
                        elif category == "분식" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            bunfood = 1)
                        elif category == "일식" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            jpfood = 1)
                        elif category == "한식" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            krfood = 1)
                        elif category == "족발/보쌈" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            jandb = 1)
                        elif category == "아시안/양식" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            aanda = 1)
                        elif category == "카페/디저트" :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            candd = 1)
                        else :
                            BigdataProcess.objects.create(
                            num = data["num"],
                            etc = 1)
                        

                    return JsonResponse({"message" : "ok"}, status=200)
                #수정
                else :
                    dt_now = datetime.now()
                    review = Review.objects.filter(sid = data["sid"], reg_time= data["predate"], num = data["num"])
                    print(review[0].rid)
                    review = Review.objects.get(rid = review[0].rid)
                    review.total_score = data["total_score"]
                    review.content = data["content"]
                    review.reg_time = dt_now.date()
                    review.save()
                    return JsonResponse({"message" : "ok"}, status=200)
            return JsonResponse({"message" : "err"}, status=400)
        return JsonResponse({"message" : "err"}, status=400)
    #거리 최적화
    @swagger_auto_schema(request_body = ShortPathRoadSerializer)
    def road_sort(self,request) :
        data = json.loads(request.body)
        if Member.objects.filter(id = data["id"]).exists():
            
            total_result_set = []
            #경로 기반으로 관광지 정보 가져오기
            select_query_set = (Landmark.objects.get(lid=data["lid1"]))
            add_set = {
                            "lid" : select_query_set.lid,
                            "landmark_name" : select_query_set.landmark_name,
                            "addr" : select_query_set.addr,
                            "latitude" : select_query_set.latitude,
                            "longitude" : select_query_set.logitude,
                            "facility" : select_query_set.facility,
                            "park" : select_query_set.park,
                            "desc" : select_query_set.desc,
                            "tel" : select_query_set.tel,
                            "theme" : select_query_set.theme,
                        }
            total_result_set.append(add_set)
            select_query_set = (Landmark.objects.get(lid=data["lid2"]))
            add_set = {
                            "lid" : select_query_set.lid,
                            "landmark_name" : select_query_set.landmark_name,
                            "addr" : select_query_set.addr,
                            "latitude" : select_query_set.latitude,
                            "longitude" : select_query_set.logitude,
                            "facility" : select_query_set.facility,
                            "park" : select_query_set.park,
                            "desc" : select_query_set.desc,
                            "tel" : select_query_set.tel,
                            "theme" : select_query_set.theme,
                        }
            total_result_set.append(add_set)
            #데이터가 1-3
            if data["lid3"] != "NULL" :
                
                select_query_set = (Landmark.objects.get(lid=data["lid3"]))
                add_set = {
                            "lid" : select_query_set.lid,
                            "landmark_name" : select_query_set.landmark_name,
                            "addr" : select_query_set.addr,
                            "latitude" : select_query_set.latitude,
                            "longitude" : select_query_set.logitude,
                            "facility" : select_query_set.facility,
                            "park" : select_query_set.park,
                            "desc" : select_query_set.desc,
                            "tel" : select_query_set.tel,
                            "theme" : select_query_set.theme,
                        }
                total_result_set.append(add_set)
            #데이터가 1-4
            if data["lid4"] != "NULL" :
                
                select_query_set = (Landmark.objects.get(lid=data["lid4"]))
                add_set = {
                            "lid" : select_query_set.lid,
                            "landmark_name" : select_query_set.landmark_name,
                            "addr" : select_query_set.addr,
                            "latitude" : select_query_set.latitude,
                            "longitude" : select_query_set.logitude,
                            "facility" : select_query_set.facility,
                            "park" : select_query_set.park,
                            "desc" : select_query_set.desc,
                            "tel" : select_query_set.tel,
                            "theme" : select_query_set.theme,
                        }
                total_result_set.append(add_set)
            #관광지 정보를 통해 최적경로 분석
            print(total_result_set)
            total_result_set = short_path(total_result_set)
            return JsonResponse({"sort_value" : total_result_set},status=200)
        else :
            return JsonResponse({"message" : "Error"}, status=400)


    # ZzimStoreCourse : 여행날짜 음식 저장
    @swagger_auto_schema(request_body = SaveOptionStoreSerializer)
    def save_option_store(self, request) :
        data = json.loads(request.body)
        
        #id확인
        if Member.objects.filter(id = data["id"]).exists():
           
            user = Member.objects.get(id=data["id"])
            #아침
            if data["flag"]==0 :
                
                #그 날짜에 데이터 존재?
                if ZzimStoreCourse.objects.filter(num=user.num, savedDate=data["savedDate"]).exists() :
                    #업데이트
                    print("업데이트")
                    Zzim = ZzimStoreCourse.objects.get(num=user.num, savedDate=data["savedDate"])
                    Zzim.sidB = data["sid"]
                    Zzim.isSavedB = "False"
                    Zzim.save()
                    return HttpResponse(status=200)
                else :
                    #추가
                    print("추가")
                    ZzimStoreCourse.objects.create(
                        num = int(user.num),
                        sidB = data["sid"],
                        isSavedB = "False",
                        savedDate =data["savedDate"]
                    )
                    return HttpResponse(status=200)
            #점심
            elif data["flag"]==1 :
                #그 날짜에 데이터 존재?
                if ZzimStoreCourse.objects.filter(num=user.num, savedDate=data["savedDate"]).exists() :
                    #업데이트
                    Zzim = ZzimStoreCourse.objects.get(num=user.num, savedDate=data["savedDate"])
                    Zzim.sidL = data["sid"]
                    Zzim.isSavedL = "False"
                    Zzim.save()
                    return HttpResponse(status=200)
                else :
                    #추가
                    ZzimStoreCourse.objects.create(
                        num = int(user.num),
                        sidL = data["sid"],
                        isSavedL = "False",
                        savedDate =data["savedDate"]
                    )
                    return HttpResponse(status=200)
            #저녁
            elif data["flag"]==2 :
                #그 날짜에 데이터 존재?
                if ZzimStoreCourse.objects.filter(num=user.num, savedDate=data["savedDate"]).exists() :
                    #업데이트
                    Zzim = ZzimStoreCourse.objects.get(num=user.num, savedDate=data["savedDate"])
                    Zzim.sidD = data["sid"]
                    Zzim.isSavedD = "False"
                    Zzim.save()
                    return HttpResponse(status=200)
                else :
                    #추가
                    ZzimStoreCourse.objects.create(
                        num = int(user.num),
                        sidD = data["sid"],
                        isSavedD = "False",
                        savedDate =data["savedDate"]
                    )
                    return HttpResponse(status=200)
            else :
                return JsonResponse({"message" : "Error"}, status=400)
        return JsonResponse({"message" : "Error"}, status=400)


    # ZzimLandCourse : 여행 경로 저장
    @swagger_auto_schema(request_body = SaveOptionLandSerializer)
    def save_option_land(self, request) :
        data = json.loads(request.body)
        
        if Member.objects.filter(id = data["id"]).exists():
            user = Member.objects.get(id=data["id"])
            if ZzimLandCourse.objects.filter(num=user.num, savedDate=data["savedDate"]).exists() :
                Zzim = ZzimLandCourse.objects.get(num=user.num, savedDate=data["savedDate"])
                Zzim.lid1 = data["lid1"]
                Zzim.lid2 = data["lid2"]
                Zzim.lid3 = data["lid3"]
                Zzim.lid4 = data["lid4"]
                Zzim.savedDate = data["savedDate"]
                Zzim.save()
                return HttpResponse(status=200)

            else :

                ZzimLandCourse.objects.create(
                    num = str(user.num),
                    #유효성 검사해야함
                    lid1 = data["lid1"],
                    lid2 = data["lid2"],
                    lid3 = data["lid3"],
                    lid4 = data["lid4"],
                    savedDate =data["savedDate"]
                    
                )
                if ZzimStoreCourse.objects.filter(num = str(user.num), savedDate= data["savedDate"]) :
                    return HttpResponse(status=200)
                else :
                    ZzimStoreCourse.objects.create(
                        num = str(user.num),
                        savedDate = data["savedDate"]
                    )
                    return HttpResponse(status=200)
        return JsonResponse({"message" : "Error"}, status=400)



    @swagger_auto_schema(request_body=UserOptionSerializer)
    def user_option(self, request):

        
        data = json.loads(request.body)
        #user_date
        #user_location
        #user_thema
        #여행 지역 기준으로 조회
        if data["user_location"] == 0 : #서울
            query_set = (Landmark.objects.filter(addr__contains="서울")) & Landmark.objects.filter(theme = data["user_thema"])
            
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
                
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    print(row[2])
                    anthor_query_set = (Landmark.objects.filter(addr__contains="서울")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        
                        slt = random.randint(0,len(anthor_query_set)-1)
                        print(slt)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="서울"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)
        elif data["user_location"] == 1 : #부산
            query_set = (Landmark.objects.filter(addr__contains="부산")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
                
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                print(data["user_thema"])
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                print(len(next_theme))
                for row in next_theme.values_list():
                    print(row)
                    anthor_query_set = (Landmark.objects.filter(addr__contains="부산")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="부산"))
            print(total_result_set)
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 2 : #인천
            query_set = (Landmark.objects.filter(addr__contains="인천")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="인천")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="인천"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 3 : #대구
            query_set = (Landmark.objects.filter(addr__contains="대구광역시")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="대구광역시")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="대구광역시"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 4 : #대전
            query_set = (Landmark.objects.filter(addr__contains="대전")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="대전")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="대전"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)
        elif data["user_location"] == 5 : #광주
            query_set = (Landmark.objects.filter(addr__contains="광주")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="광주")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="광주"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 ��리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)
        elif data["user_location"] == 6 : #울산
            query_set = (Landmark.objects.filter(addr__contains="울산")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="울산")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="울산"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 7 : #제주
            query_set = (Landmark.objects.filter(addr__contains="제주")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="제주")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="제주"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 8 : #경기
            query_set = (Landmark.objects.filter(addr__contains="경기")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="경기")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="경기"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)
        elif data["user_location"] == 9 : #강원
            query_set = (Landmark.objects.filter(addr__contains="강원")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="강원")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="강원"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 10 : #충남, 충청남도
            query_set = (Landmark.objects.filter(addr__contains="충남") | Landmark.objects.filter(addr__contains="충청남도")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="충남") | Landmark.objects.filter(addr__contains="충청남도")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="충남") | Landmark.objects.filter(addr__contains="충청남도"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 11 : #충북, 충청북도
            query_set = (Landmark.objects.filter(addr__contains="충북") | Landmark.objects.filter(addr__contains="충청북도")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="충북") | Landmark.objects.filter(addr__contains="충청북도")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="충북") | Landmark.objects.filter(addr__contains="충청북도"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 12 : #경남, 경상남도
            query_set = (Landmark.objects.filter(addr__contains="경남") | Landmark.objects.filter(addr__contains="경상남도")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="경남") | Landmark.objects.filter(addr__contains="경상남도")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="경남") | Landmark.objects.filter(addr__contains="경상남도"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 13 : #경북, 경상북도
            query_set = (Landmark.objects.filter(addr__contains="경북") | Landmark.objects.filter(addr__contains="경상북도")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="경북") | Landmark.objects.filter(addr__contains="경상북도")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="경북") | Landmark.objects.filter(addr__contains="경상북도"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            print(total_result_set)
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 14 : #전북, 전라북도
            query_set = (Landmark.objects.filter(addr__contains="전북") | Landmark.objects.filter(addr__contains="전라북도")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="전북") | Landmark.objects.filter(addr__contains="전라북도")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="전북") | Landmark.objects.filter(addr__contains="전라북도"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)

        elif data["user_location"] == 15 : #전남, 전라남도
            query_set = (Landmark.objects.filter(addr__contains="전남") | Landmark.objects.filter(addr__contains="전라남도")) & Landmark.objects.filter(theme = data["user_thema"])
            total_result_set = []
            result_set = []
            if len(query_set) > 0 : #값이 존재
                #랜덤수 생성
                slt = random.randint(0,len(query_set)-1)
                #대입
                select = query_set[slt]
                #수정
                add_set = { "lid" : select.lid,
                            "landmark_name" : select.landmark_name,
                            "addr" : select.addr,
                            "latitude" : select.latitude,
                            "longitude" : select.logitude,
                            "facility" : select.facility,
                            "park" : select.park,
                            "desc" : select.desc,
                            "tel" : select.tel,
                            "theme" : select.theme
                            }
                #위도 경도기준으로 가까운거 3개 뽑기
                #for row in query_set.values_list():
                total_result_set.append(add_set)
            else : #값이 존재하지 않음 다른거 1개 골라서 추천해야 함
                next_theme = RScoreTable.objects.filter(t1 = data["user_thema"]).order_by("-score")
                for row in next_theme.values_list():
                    anthor_query_set = (Landmark.objects.filter(addr__contains="전남") | Landmark.objects.filter(addr__contains="전라남도")) & Landmark.objects.filter(theme = row[2])
                    if len(anthor_query_set) > 0 :
                        slt = random.randint(0,len(anthor_query_set)-1)
                        #대입
                        select = anthor_query_set[slt]
                        #수정
                        add_set = { "lid" : select.lid,
                                    "landmark_name" : select.landmark_name,
                                    "addr" : select.addr,
                                    "latitude" : select.latitude,
                                    "longitude" : select.logitude,
                                    "facility" : select.facility,
                                    "park" : select.park,
                                    "desc" : select.desc,
                                    "tel" : select.tel,
                                    "theme" : select.theme
                                    }
                        
                        total_result_set.append(add_set)
                        break
            #다른 여행지 추가
            
            select_query_set = (Landmark.objects.filter(addr__contains="전남") | Landmark.objects.filter(addr__contains="전라남도"))
            anthor_land = anthor_land_ck(select_query_set, total_result_set,data)
            curr = 0
            for row in anthor_land :
                if curr > 2 :
                    add_set = {
                        "lid" : row["lid"],
                        "landmark_name" : row["landmark_name"],
                        "addr" : row["addr"],
                        "latitude" : row["latitude"],
                        "longitude" : row["longitude"],
                        "facility" : row["facility"],
                        "park" : row["park"],
                        "desc" : row["desc"],
                        "tel" : row["tel"],
                        "theme" : row["theme"],
                        "score" : row["score"]
                    }
                    result_set.append(add_set)
                else :
                    add_set = {
                            "lid" : row["lid"],
                            "landmark_name" : row["landmark_name"],
                            "addr" : row["addr"],
                            "latitude" : row["latitude"],
                            "longitude" : row["longitude"],
                            "facility" : row["facility"],
                            "park" : row["park"],
                            "desc" : row["desc"],
                            "tel" : row["tel"],
                            "theme" : row["theme"],
                            "score" : row["score"]
                        }
                    total_result_set.append(add_set)
                curr+=1
            #여행지 거리별 최적화
            total_result_set = short_path(total_result_set)
            return JsonResponse({"recommend" : total_result_set,"recommend_other" : result_set},status=200)
  
    ######## hotkeyword15 #############################################
    #1  lid1,lid4 위경도 가져옴
    #2. 두지점의 중간점을 중심으로 반경설정, 반경안에 있는 들어있는 식당(sid) 조회 리스트
    #3. 리스트에 있는 sid > 리뷰 조회
    #4. 리뷰 다 붙임
    #5. api에 넣고 키워드 추출
    #6. 상위 15개 리턴
    ###

        #return JsonResponse({"message" : "err"}, status=400)    

    @swagger_auto_schema(request_body=  KeywordSerializer) #ehdrb
    def main_storelist(self, request):
        
        data = json.loads(request.body) 
        key  = data["keyword"]
        lat  = data["latitude"]
        log = data["logitude"]
        storesort = []

        condition = ( #반경 1km
                    Q(latitude__range  = (lat - 0.005, lat + 0.005)) &     #lat 0.01 = 1km /  #lat 0.1 = 10km
                    Q(logitude__range = (log - 0.0075, log + 0.0075))      #log 0.015 = 1km / #log 0.150 = 10km
                )
 
        store = Store.objects.filter(address__contains = key).order_by('-review_avg')[:50]
       
        serializer = StoreSerializer(store, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body = LatLogSerializer)
    def hot_keyword_15(self, request):
        data = json.loads(request.body) 
        lat1  = data["latitude"]
        log1 = data["logitude"]
        

        # lat4  = float(request.GET.get('latitude', None))
        # log4 = float(request.GET.get('longitude', None))

        # midlat = (lat1 + lat4)/2
        # midlog = (log1 + log4)/2

        # position  = (midlat,midlog)
        condition = ( #반경 2km
                    Q(latitude__range  = (lat1 - 0.02, lat1 + 0.02)) &     #lat 0.01 = 1km /  #lat 0.1 = 10km
                    Q(logitude__range = (log1 - 0.03, log1 + 0.03))      #log 0.015 = 1km / #log 0.150 = 10km
                )
       
        appendreview =''

        #query_set = Review.objects.filter(sid__in=Store.objects.filter(condition).filter(sid='2239'))
        query_set = Review.objects.filter(sid__in=Store.objects.filter(condition))

        if query_set.exists():
            #print("잇다")
            #print(query_set)
            #print(query_set[0].content)
            #print(len(query_set))
            for i in range(len(query_set)):
                #print(query_set[i].sid + " " + query_set[i].content) ##
                appendreview += query_set[i].content + " "

        else:
            print("없다")

        #print(appendreview)
        print('{}개의 리뷰 검색완료'.format(len(query_set)))
        rst = keyword_mining(appendreview)
        print("---------------------")
        print(rst)
        result_set = []
        for i in range(len(rst)) :
            add_set = {
                "keyword" : rst[i]
            }
            result_set.append(add_set)
        print("----------------------")
        return JsonResponse({"message" : result_set}, status=200)
        # circle_store_infos = [info for info in store_infos
        #                                 if haversine( position, (target.lat, target.log)) <= 2            ]

        # circle_store_infos[0] , circle_store_infos[1].....
        #return Response(, status=status.HTTP_204_NO_CONTENT)
        
                
    #####################################################
    #1. 키워드를 받는다.
    #2. 받은 키워드를 리뷰에 포함하고 있는 상점리스트 + 평점순 출력
    #3. 리스트 상위 n개 리턴
    ##
    # 점수 부여하고 점수순으로 정렬 
    
    @swagger_auto_schema(request_body = KeywordSerializer)
    def keyword_storelist(self, request):
        data = json.loads(request.body)
        key  = data["keyword"]
        lat = data["latitude"]
        log = data["logitude"]
        storesort = []
        
        #Store.objects.filter(sid = sid)

        ## 이친구를 ORM 해야된다 
        # select a.sid,avg(total_score) avg from (select s.sid,s.store_name,address,total_score,content from stores s,reviews r
        #where s.sid = r.rid and r.content like '%송정%' order by s.sid) a group by a.sid order by avg desc; 
    
        # 
        # 1. select s.sid,s.store_name,address,total_score,content 
        #   from stores s,reviews r
        #   where s.sid = r.ㄴid and r.content like '%송정%'  
        #   order by s.sid
        
        
       
        # #query_set = Review.objects.filter(sid__in=Store.objects.filter(condition).filter(sid='2239'))
        # review = Review.objects.filter(sid__in=Store.objects.filter(condition))

        condition = ( #반경 2km
                    Q(latitude__range  = (lat - 0.05, lat + 0.05)) &     #lat 0.01 = 1km /  #lat 0.1 = 10km
                    Q(logitude__range = (log - 0.075, log + 0.075))      #log 0.015 = 1km / #log 0.150 = 10km
                )
       
        #query_set = Review.objects.filter(sid__in=Store.objects.filter(condition).filter(sid='2239'))
        review = Review.objects.filter(sid__in=Store.objects.filter(condition, review_avg__gte = 3)).filter(content__contains = key)
        stores = Store.objects.filter(condition, review_avg__gte = 3).values()
        stores = pd.DataFrame(stores)
        # ttt = stores["sid"] == 1176
        # storex = stores[ttt]
        # print(storex)
        review = sorted(review, key=lambda review: review.sid)
        
        #print(len(review))
        # 해당 글자가 포함된 리뷰 -> 중복 x sid가 잇어야함
        
        #review = Review.objects.filter(content__contains = key) # '송정'을 content에 포함하고 있는 리뷰행  
       
        #print(review.values_list)         #(송정을 포함하고 있는 리뷰)를 가진 상점의 모든 리뷰
        pre  = -1
        for row in review : #row[1] 리뷰행에서 sid 값
            if pre == row.sid :
                continue
            pre = row.sid
            step = stores["sid"] == int(row.sid)
            
            store_list = stores[step]
            store_list = store_list.values.tolist()
            
            add_set = {
                        "sid" : store_list[0][0],
                        "store_name" : store_list[0][1],
                        "branch" : store_list[0][2],
                        "area" : store_list[0][3],
                        "tel" : store_list[0][4],
                        "address" : store_list[0][5],
                        "latitude" : store_list[0][6],
                        "logitude" : store_list[0][7],
                        "review_cnt" : store_list[0][8],
                        "category" : store_list[0][10],
                        "review_avg" : store_list[0][11],
                    }
            storesort.append(add_set)
            
                
                
        
        storesort = sorted(storesort, key=lambda storesort: storesort["review_avg"], reverse= True)
        result_set = []
        # 20개넘으면 > 20번만 반복
        # 20개 안되면 > len(storesort) 만큼 반복
        print(len(storesort))
        if(len(storesort)>=20):    
            for i in range(20):
                result_set.append(storesort[i])
        else:
            for i in range(len(storesort)):
                result_set.append(storesort[i])           
        return JsonResponse({"message" : result_set}, status=200)

      
#키워드 마이닝 
def keyword_mining(question):
    url = 'http://svc.saltlux.ai:31781'
    headers = {'Content-Type': 'application/json; charset:utf-8'}
    params ={
        "key": "e87ac2a2-d4e3-48ca-9100-614f3fdba6df",
        "serviceId": "00116013830",
        'argument': {
            "question": question,
        }
    }
    response = json.loads(requests.post(url, headers=headers, data=json.dumps(params)).text)

    result = []
    #keyweight = {"keyword":[],"weight":[]}

    k = 0
    for i in response['return_object']['keylists']:   #[{"keyword":"해운대","weight":0.01339"},{"keyword":"해운대","weight":0.12349"}]
        #result.append(i['keyword'])
        #   ==>0.013391831, 0.009553034, 0.007839888, 0.0077515743, 0.007545752
        calc_keyword = i['keyword'].replace("_", " ")

        calc_weight = i['weight']
        calc_weight *= 1000
        if calc_weight >= 10: 
            calc_weight = 10
        calc_weight=int(calc_weight)

        add_set = {
            "keyword" : calc_keyword,
            "value" : calc_weight,
        }
        result.append(add_set) 
        #print(result)       
        k += 1
        if k == 15:
            break
    return result

def anthor_land_ck(select_query_set, total_result_set,data):
    anthor_land = []
    for row in select_query_set.values_list() :
        if total_result_set[0]["lid"] != row[0] :
            score = 0
            #테마 점수
            next_theme = (RScoreTable.objects.filter(t1 = data["user_thema"]) & RScoreTable.objects.filter(t2 = row[9])).values_list()
            score = float(next_theme[0][3])
            
            #거리 점수
            # 위경도 입력 
            
            curr = (float(total_result_set[0]["latitude"]), float(total_result_set[0]["longitude"])) #Latitude, Longitude
            arrive = (float(row[3]), float(row[4])) 
            # 거리 계산 
            km = haversine(curr, arrive, unit = 'km')
            km = round(km,2)
            if km > 50 :
                continue
            if km == 0 :
                km = 0.7
            else :
                km = 1/km
            score = score + km
            score = round(score,2)
            
            add_set = {
                "lid" : row[0],
                "landmark_name" : row[1],
                "addr" : row[2],
                "latitude" : row[3],
                "longitude" : row[4],
                "facility" : row[5],
                "park" : row[6],
                "desc" : row[7],
                "tel" : row[8],
                "theme" : row[9],
                "score" : score
            }
            anthor_land.append(add_set)
    anthor_land = sorted(anthor_land, key=lambda anthor_land: anthor_land["score"], reverse=True)
    return anthor_land

    #     def 
rst = []
flag = []
min_num = 0
def short_path(result_set):
    global rst, ck, min_num, flag
    map = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    size = len(result_set)
    for i in range(len(result_set)) :
        for j in range(i+1,len(result_set)) :
            
            data = {
                "startX" : result_set[i]["longitude"],
                "startY" : result_set[i]["latitude"],
                "endX" : result_set[j]["longitude"],
                "endY" : result_set[j]["latitude"],
                "reqCoordType" : "WGS84GEO",
                "resCchOption" : "0",
                "trafficInfo" : "N"
            }
            
            data = json.dumps(data)
            randomkey = random.randint(0,len(T_KEY)-1)
            headers = {'Content-Type': 'application/json', 'appKey': T_KEY[randomkey]}
            url = "https://apis.openapi.sk.com/tmap/routes?version=1&format=json&callback=result"
            res = requests.post(url, data=data, headers=headers)
            json_object = res.json()
            totalDistance = json_object["features"][0]["properties"]["totalDistance"]
            map[i][j] = totalDistance
            map[j][i] = totalDistance
    print(map)
    rst = [-1,-1,-1,-1]
    ck = [-1,-1,-1,-1]
    flag = [-1,-1,-1,-1]
    min_num = 1000000
    dfs(0, 0, map, 0, size)
    st_path = copy.deepcopy(rst)
    st_distance = min_num
    return_set = []
    for i in range(size) :
        return_set.append(result_set[st_path[i]])
    if len(return_set) != 4 :
        for i in range(4) :
            if len(return_set) == 4 :
                break;
            add_set = {
                "lid" : "NULL"
            }
            return_set.append(add_set)
    add_set = {"one_two" : map[st_path[0]][st_path[1]]/1000, "two_three" : map[st_path[1]][st_path[2]]/1000, "three_four" : map[st_path[2]][st_path[3]]/1000, "total" : st_distance/1000}
    return_set.append(add_set)
    return return_set
    # print(sort_path)
    
def dfs(dep, dist, map, pre, size):
    global rst, ck, min_num, flag
    if dep == size :
        
        if min_num>dist :
            print(dist)
            print(ck)
            min_num = dist
            rst = copy.deepcopy(ck)
            return
        return
    for i in range(size) :
        # 방문했던점이면 건너뜀
        if flag[i] != -1 :
            continue
        flag[i] = 0
        ck[dep] = i
        if dep == 0 :
            dfs(dep+1, dist, map, i,size)
        else :
            dfs(dep+1, dist+map[pre][i], map, i,size)
        flag[i] = -1
        ck[dep] = -1
    
# Create your views here.

    