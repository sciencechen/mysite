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


def getmindmap(request):
    # 获取所有用户
    all_users = baidu_model.objects.all()

    # 获取有条件的获取用户
    user = baidu_model.objects.filter(title='1')

    # return HttpResponse(all_users[1].title)
    return HttpResponse(user[0].url)
    # return HttpResponseRedirect(user[0].url)


class MindMapView(View):

    def get(self, request):
        """
               查询所有图书
               路由：GET /books/
               """
        queryset = baidu_model.objects.all()
    #     book_list = []
    #     for book in queryset:
    #         book_list.append({
    #             'id': book.id,
    #             'title': book.title,
    #             'url': book.url,
    #             'parentid': book.parentid,
    #         })
    #     return JsonResponse(book_list, safe=False)
    #     # return HttpResponse("this is post of mindmap-django server")
    #
    #     return JsonResponse("this is get of mindmap-django server,hhhhhh", safe=False)
    #
    #     pass
    #
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


# -------------------------------------------------------------------------
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
