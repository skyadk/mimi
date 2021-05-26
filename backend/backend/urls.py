"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
#from django.conf.urls import url
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


#drf_yasg swagger정의 https://drf-yasg.readthedocs.io/en/stable/readme.html#openapi-3-0-note 공식문서참조
schema_view = get_schema_view(
    #info : Swagger API 정보 객체로써 생략시 기본값은 DEFAULT_INFO
    openapi.Info(
        title="Swagger mimi API",
        default_version = "v1",
        description="Swagger mimi API 문서",
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="test", email="test@test.com"), 
        license=openapi.License(name="Test License"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)


# fmt: off
urlpatterns = [
    #api사양의 JSON, YAML보기
    #url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #api사양의 ReDoc보기
    #path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #api사양의 swagger-ui보기
    path("mimi/swagger/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    path("mimi/admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("mimi/member/", include(("member.urls", "member"))), #member 앱의 세부 url은 member앱의 urls에서 관리
    path("mimi/recommendroad/", include(("recommendroad.urls", "recommendroad")))
] 
# fmt: on
