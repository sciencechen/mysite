import os
import uuid

import simplejson
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.utils import json

from .serializers import baidu_modelSerializer

from .models import baidu_model
from django.views import View


def index(request):
    return HttpResponse("this is mindmap-django server")

def getrootlist(request):
    """
   获取根节点目录
   路由： GET  /books/<pk>/
   """
    print('-------------')
    print('获取根节点目录')
    print('-------------')

    try:
        queryset = baidu_model.objects.all()
    except baidu_model.DoesNotExist:
        return HttpResponse(status=404)

    root_set = set()
    for node in queryset:
        root_set.add(node.root)

    print(root_set)

    root_list = []
    for value in root_set:
        root_list.append({
            "value": value
        })


    # 最后返回
    return JsonResponse(root_list, safe=False)



def deletenode(request):
    """
   删除图书
   路由： POST deletenode/
   """
    # nodelist = request.POST.get('nodelist', 123)
    nodejson = simplejson.loads(request.body)
    predata = nodejson['predata']['data']
    laterdata = nodejson['laterdata']['data']

    print(predata)
    print(laterdata)

    predatamid = []
    laterdatamid = []

    for node in predata:
        predatamid.append(node['id'])

    for node in laterdata:
        laterdatamid.append(node['id'])



    deletenodemidlist = set(predatamid).difference(laterdatamid)
    print('被删除节点的mid', deletenodemidlist)
    print('被删除节点的数量： ', len(deletenodemidlist))

    for mid in deletenodemidlist:
        try:
            queryset = baidu_model.objects.filter(mid=mid)
        except baidu_model.DoesNotExist:
            return HttpResponse(status=404)
        queryset.delete()


    # return JsonResponse({'id' :'nihao'})
    return HttpResponse(status=204)


def expandnode(request):
    """
   拓展节点
   路由： GET  /books/<pk>/
   """
    mid = request.GET.get('mid', '0')
    exword = request.GET.get('exword', '0')
    splice = request.GET.get('splice', '0')

    print('-------------')
    print('拓展节点')
    print(mid)
    print(exword)
    print(splice)
    print('-------------')

    try:
        queryset = baidu_model.objects.filter(mid=mid)
    except baidu_model.DoesNotExist:
        return HttpResponse(status=404)

    hnode = baidu_model.objects.create(
        root=queryset[0].root,
        mid=uuid.uuid1(),
        title=exword,
        url=00,
        parentid=mid,
        nodetype="h"
    )



    # 要同时执行，否则执行的每一条命令是作用在当前目录下，
    # 所以要cd转跳的瞬间（os.system前半句还未执行完的瞬间）
    # 把python run.py执行完
    # 教训： 因为用的是cmd命令来传递参数，所以字符串不可以有空格，多一个空格就会改变后面命令的意思
    if splice == '带上节点':
        keyword = exword + "," + queryset[0].title
    else:
        keyword = exword
    parentid = str(hnode.mid)
    root = queryset[0].root

    cmd = 'cd C:/chenjimiao/project/python/aiTeacherPlan/project/crawler/ && scrapy crawl baidu_spider -a keyword=' + keyword + ' -a parentid=' + parentid + ' -a root=' + root
    # cmd = 'cd C:/chenjimiao/project/python/aiTeacherPlan/project/crawler/ && scrapy crawl baidu_spider -a keyword=' + keyword + ' -a parentid=' + parentid + ' -a root=' + "testroot"

    test = os.system(cmd)

    print('返回根节点为', queryset[0].root, '的jsmind')

    try:
        queryset = baidu_model.objects.filter(root=root)
    except baidu_model.DoesNotExist:
        return HttpResponse(status=404)

    node_list = []
    for node in queryset:
        node_list.append({
            'id': node.id,
            'title': node.title,
            'url': node.url,
            'parentid': node.parentid,
            'mid': node.mid,
            'root': node.root,
            'nodetype': node.nodetype

        })
    # 最后返回
    return JsonResponse(node_list, safe=False)



def getmindmap(request):
    # 获取所有用户
    all_users = baidu_model.objects.all()

    # 获取有条件的获取用户
    user = baidu_model.objects.filter(title='1')

    # return HttpResponse(all_users[1].title)
    return HttpResponse(user[0].url)
    # return HttpResponseRedirect(user[0].url)


def creatroot(request):
    """
   创建根节点
   路由： GET  /books/<pk>/
   """
    topic = request.GET.get('topic', '0')
    type = request.GET.get('type', '0')
    url = request.GET.get('url', '0')

    print('-------------')
    print('创建根节点')
    print('-------------')

    root = baidu_model.objects.create(
        root=topic,
        mid=uuid.uuid1(),
        title=topic,
        url=url,
        parentid='isroot',
        nodetype=type
    )

    # 最后返回
    return JsonResponse({
            'id': root.id,
            'topic': root.title,
            'url': root.url,
            'parentid': root.parentid,
            'mid': root.mid,
            'root': root.root,
            'nodetype': root.nodetype

        }, status=201)


def searchbyroot(request):
    """
   通过root根节点寻找同一类的节点集合
   路由： GET  /books/<pk>/
   """
    searchbyroot = request.GET.get('searchbyroot', '0')
    print('-------------')
    print('通过root寻找jsmind： '+searchbyroot)
    print('-------------')

    try:
        queryset = baidu_model.objects.filter(root=searchbyroot)
    except baidu_model.DoesNotExist:
        return HttpResponse(status=404)

    node_list = []
    for node in queryset:
        node_list.append({
            'id': node.id,
            'title': node.title,
            'url': node.url,
            'parentid': node.parentid,
            'mid': node.mid,
            'root': node.root,
            'nodetype': node.nodetype

        })
    # 最后返回
    return JsonResponse(node_list, safe=False)




class BooksAPIVIew(View):
    """
   查询所有图书、增加图书
   """
    def get(self, request):
        """
       查询所有图书
       路由：GET /books/
       """
        queryset = baidu_model.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'title': book.title,
                'url': book.url,
                'parentid': book.parentid,
                'mid': book.mid,
                'root': book.root,
                'nodetype': book.nodetype

            })
        # 定一个变量接收返回前端的数据
        # response = HttpResponse({'message': '验证码不能重复发送'})
        response = JsonResponse(book_list, safe=False)
        # 在变量后加上["Access-Control-Allow-Origin"] = "*" or ["Access-Control-Allow-Origin"] = "指定一个域名"
        response["Access-Control-Allow-Origin"] = "*"
        response["access-control-allow-headers"] = "Authorization, Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, X-File-Type, Cache-Control, Origin"
        response["access-control-allow-methods"] = "GET, POST, OPTIONS, PUT, DELETE"
        response["access-control-expose-headers"] = "Authorization"

        # 最后返回
        return JsonResponse(book_list, safe=False)

        # return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
       新增图书
       路由：POST /books/
       """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = baidu_model.objects.create(
            btitle=book_dict.get('title'),
            url=book_dict.get('url')

        )

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'url': book.url,
            'parentid': book.parentid,
            'mid': book.mid,
            'root': book.root,
            'nodetype': book.nodetype

        }, status=201)


class BookAPIView(View):
    def get(self, request, pk):
        """
       获取单个图书信息
       路由： GET  /books/<pk>/
       """
        try:
            book = baidu_model.objects.get(pk=pk)
        except baidu_model.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'url': book.url,
            'parentid': book.parentid,
            'mid': book.mid,
            'root': book.root,
            'nodetype': book.nodetype

        })

    def put(self, request, pk):
        """
       修改图书信息
       路由： PUT  /books/<pk>
       """
        try:
            book = baidu_model.objects.get(pk=pk)
        except baidu_model.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.title = book_dict.get('title')
        book.url = book_dict.get('url')

        book.save()

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'url': book.url,
            'parentid': book.parentid,
            'mid': book.mid,
            'root' : book.root,
            'nodetype': book.nodetype

        })

    def delete(self, request, pk):
        """
       删除图书
       路由： DELETE /books/<pk>/
       """
        try:
            book = baidu_model.objects.get(pk=pk)
        except baidu_model.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()
        return JsonResponse({'id' :'nihao'})
        return HttpResponse(status=204)


# -------------------------------------------------------------------------


# ViewSets定义视图的行为。
class BaiduViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径,hahahah
    """
    queryset = baidu_model.objects.all()
    serializer_class = baidu_modelSerializer


# -------------------------------------------------------------------------

class MindMapView(View):

    def get(self, request):
        """
               查询所有图书
               路由：GET /books/
               """
        queryset = baidu_model.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'title': book.title,
                'url': book.url,
                'parentid': book.parentid,
            })
        return JsonResponse(book_list, safe=False)
        # return HttpResponse("this is post of mindmap-django server")

        return JsonResponse("this is get of mindmap-django server,hhhhhh", safe=False)

        pass

    # def post(self, request):
    #
    #     return HttpResponse("this is post of mindmap-django server")
    #
    #     pass
    #
    # def delete(self, request, *args, **kwargs):
    #     pk = kwargs.get("id")
    #     data = request.data
    #     if pk:
    #         inst = baidu_model.objects.filter(id=pk).first()
    #         if inst:
    #             inst.delete()
    #             return HttpResponse(data={"code": 200, "msg": "删除ok"})
    #         else:
    #             return HttpResponse(data={"code": 404, "msg": "删除失败,不存在!"})
    #     else:
    #         ids = data.get("ids")
    #         if isinstance(ids, list):
    #             objs = baidu_model.objects.filter(id__in=ids)
    #             objs.delete()
    #             return HttpResponse(data={"code": 200, "msg": "删除ok"})



