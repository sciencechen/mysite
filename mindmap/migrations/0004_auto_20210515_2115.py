# Generated by Django 3.2.2 on 2021-05-15 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mindmap', '0003_rename_baidu_model_baidu'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='baidu',
            new_name='baidu_model',
        ),
        migrations.AlterModelOptions(
            name='baidu_model',
            options={'verbose_name': '百度搜索结果', 'verbose_name_plural': '百度搜索结果'},
        ),
        migrations.AlterModelTable(
            name='baidu_model',
            table='mindmap_baidu',
        ),
    ]
