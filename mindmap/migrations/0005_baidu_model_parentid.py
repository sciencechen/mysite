# Generated by Django 3.2.2 on 2021-05-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindmap', '0004_auto_20210515_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='baidu_model',
            name='parentid',
            field=models.CharField(default='root', max_length=20, verbose_name='父节点'),
        ),
    ]
