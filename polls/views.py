from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, Group
from .models import Question
from rest_framework import viewsets
from polls.serializers import UserSerializer, GroupSerializer, QuestionSerializer


def index(request):
    return HttpResponse("hello,world.You're at the polls index\n"
                        "我是陈继淼")


# ViewSets定义视图的行为。
class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer