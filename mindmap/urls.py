from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='mind'),
    path('get/', views.getmindmap, name='get'),

    # .as_view()非常重要，不可或缺
    path(r'test/', views.MindMapView.as_view()),

    re_path(r'^books/$', views.BooksAPIVIew.as_view()),
    re_path(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view()),

    path('startscraler/', views.startcrawler, name='启动爬虫'),
    path('searchbyroot/', views.searchbyroot, name='通过root根节点寻找同一类的节点集合'),
    path('creatroot/', views.creatroot, name='创建根节点'),
    path('expandnode/', views.expandnode, name='拓展节点'),

]