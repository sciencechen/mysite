from django.db import models


# Create your models here.


class baidu_model(models.Model):
    # 根节点主题，如：深度学习
    root = models.CharField(max_length=50, verbose_name='根节点', default="root")
    # UUID
    mid = models.CharField(max_length=40, verbose_name='jsmind的id')
    title = models.CharField(max_length=200, verbose_name='标题')
    url = models.CharField(max_length=200, verbose_name='百度重定向链接')
    # 父节点的UUID
    parentid = models.CharField(max_length=40, verbose_name='父节点', default="root")
    # h:文本节点
    # a:url节点
    # img:图片节点
    # video：视频节点
    # audio：音频节点
    nodetype = models.CharField(max_length=20, verbose_name='节点类型', default="a")

    # def delete(self, using=None, keep_parents=False):
    #     self.is_delete = True
    #     self.save()

    class Meta:
        db_table = 'mindmap_baidu'
        verbose_name = '百度搜索结果'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '这是title为\'{0}\'的model对象,url为{1}\n'.format(self.title, self.url)
