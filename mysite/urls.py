"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf.urls import url
from polls import views
from mindmap import views as view2

# 路由器提供一个简单自动的方法来决定URL的配置。
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'Questions', views.QuestionViewSet)
router.register(r'baidu', view2.BaiduViewSet)
#
# 通过URL自动路由来给我们的API布局。
# 此外，我们还要把登录的URL包含进来。

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    path('mindmap/', include('mindmap.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'', include(router.urls)),

]
