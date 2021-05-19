from rest_framework import serializers
from .models import baidu_model


# 序列化器是用来定义API的表示形式。
class baidu_modelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = baidu_model
        fields = ('id', 'title', 'url')

