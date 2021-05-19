from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='mind'),
    path('get/', views.getmindmap, name='get'),

    # .as_view()非常重要，不可或缺
    path(r'test/', views.MindMapView.as_view()),

    re_path(r'^books/$', views.BooksAPIVIew.as_view()),
    re_path(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view())
]