
from django.db import models
from member.models import Member
from datetime import datetime



#Create your models here.
#r v s

#store 
class Store(models.Model):
    
    sid = models.CharField(max_length=30, primary_key=True)
    store_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=100, null=True)
    logitude = models.CharField(max_length=100, null=True)
    review_cnt = models.IntegerField(default=0)
    review_sum = models.IntegerField(default=0)
    category = models.CharField(max_length=100, null=True)
    review_avg = models.DecimalField(decimal_places=2,max_digits=4)



    class Meta:
        db_table = "stores"

#menu`  6asd
class Menu(models.Model):
    
    mid = models.CharField(max_length=30, primary_key=True)
    sid = models.CharField(max_length=39, null=True)    
    menu_name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=100, null=True)
    
    class Meta:
        db_table = "menus"

#review 
class Review(models.Model):
    
    rid = models.CharField(max_length=30, primary_key=True)
    sid = models.CharField(max_length=30, null=True)
    #sid = models.ForeignKey(Store, related_name="reviewss",on_delete=models.CASCADE,null=False)
    num = models.CharField(max_length=30, null=True)

    total_score = models.CharField(max_length=30, null=True)
    content = models.TextField()
    reg_time = models.TextField()


    class Meta:
        db_table = "reviews"

#landmark 관광지정보 
class Landmark(models.Model):
    
    lid = models.CharField(max_length=30, primary_key=True)
    landmark_name = models.CharField(max_length=200)
    addr = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=200, null=True)
    logitude = models.CharField(max_length=200, null=True)
    facility = models.CharField(max_length=200, null=True)                    #편의시설정보 varchar(200)
    park = models.CharField(max_length=200, null=True)                        #주차가능대수 varchar(200)
    desc = models.TextField()                                      #관광지 소개 text
    tel = models.CharField(max_length=200, null=True)
    theme = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "landmarks"

#맛집코스
class ZzimStore(models.Model):
    
    id = models.IntegerField(primary_key=True)
    num = models.CharField(max_length=30, null=True)  #사용자구분번호 ( members.num )
    sid = models.CharField(max_length=30, null=True)                       #아침코스(식당)  ( stores.sid )           

    class Meta:
        db_table = "zzimStores"

#맛집코스
class ZzimStoreCourse(models.Model):
    
    id = models.IntegerField(primary_key=True)
    num = models.CharField(max_length=30, null=True)  #사용자구분번호 ( members.num )
    sidB = models.CharField(max_length=30, null=True)                       #아침코스(식당)  ( stores.sid )
    isSavedB = models.CharField(max_length=30, null=True)                     #아침저장여부                 
    sidL = models.CharField(max_length=30, null=True)                       #점심코스(식당)  ( stores.sid )
    isSavedL = models.CharField(max_length=30, null=True)                    #점심저장여부                 
    sidD = models.CharField(max_length=30, null=True)                        #저녁코스(식당)  ( stores.sid )
    isSavedD = models.CharField(max_length=30, null=True)                     #저녁저장여부  
    savedDate = models.CharField(max_length=100, null=True)                   #코스 저장일자                  

    class Meta:
        db_table = "zzimStoreCourses"

#관광지코스
class ZzimLandCourse(models.Model):

    id = models.IntegerField(primary_key=True)
    num = models.CharField(max_length=30, null=True)   #사용자구분번호 ( members.num )
    lid1 = models.CharField(max_length=30, null=True)                 #1코스
    lid2 = models.CharField(max_length=30, null=True)                 #2코스
    lid3 = models.CharField(max_length=30, null=True)                 #3코스
    lid4 = models.CharField(max_length=30, null=True)                 #4코스
    isSaved = models.CharField(max_length=30, null=True)                      #코스저장여부
    savedDate = models.CharField(max_length=100, null=True, default=datetime.now())                   #코스 저장일자                   

    class Meta:
        db_table = "zzimLandCourses"

class RScoreTable(models.Model):
  t1 = models.CharField(max_length=50, null=True)
  t2 = models.CharField(max_length=50, null=True)
  score = models.DecimalField(decimal_places=3,max_digits=4)
  
  class Meta:
        db_table = "rScoreTables"

# 빅데이터 처리를 위한 count
class BigdataCount(models.Model) :
    num = models.IntegerField(primary_key=True)
    jandt = models.IntegerField(default=0)
    candd = models.IntegerField(default=0)
    chfood = models.IntegerField(default=0)
    chicken = models.IntegerField(default=0)
    pizza = models.IntegerField(default=0)
    fastfood = models.IntegerField(default=0)
    bunfood = models.IntegerField(default=0)
    jpfood = models.IntegerField(default=0)
    krfood = models.IntegerField(default=0)
    jandb = models.IntegerField(default=0)
    aanda = models.IntegerField(default=0)
    etc = models.IntegerField(default=0)
    sumcount = models.IntegerField(default=0)
    class Meta:
        db_table = "BigdataCounts"


class BigdataProcess(models.Model) :
    num = models.FloatField(primary_key=True)
    jandt = models.FloatField(default=0)
    candd = models.FloatField(default=0)
    chfood = models.FloatField(default=0)
    chicken = models.FloatField(default=0)
    pizza = models.FloatField(default=0)
    fastfood = models.FloatField(default=0)
    bunfood = models.FloatField(default=0)
    jpfood = models.FloatField(default=0)
    krfood = models.FloatField(default=0)
    jandb = models.FloatField(default=0)
    aanda = models.FloatField(default=0)
    etc = models.FloatField(default=0)
    
    class Meta:
        db_table = "BigdataProcesss"