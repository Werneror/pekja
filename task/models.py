from django.db import models
from asset.models import Project


class Tool(models.Model):

    name = models.CharField(verbose_name='工具名称', max_length=100)
    link = models.URLField(verbose_name='项目链接', null=True, blank=True)
    type = models.CharField(verbose_name='记录类型', max_length=50)
    parse_class_name = models.CharField(verbose_name='解析类名', max_length=50)
    command = models.CharField(verbose_name='调用命令', max_length=500)
    comment = models.CharField(verbose_name='备注', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工具表'
        verbose_name_plural = verbose_name


class Task(models.Model):

    name = models.CharField(verbose_name='任务名', max_length=100)
    project = models.ForeignKey(verbose_name='所属项目', to=Project, on_delete=models.CASCADE)
    tool = models.ForeignKey(verbose_name='工具', to=Tool, on_delete=models.CASCADE)
    input = models.TextField(verbose_name='输入')
    dispatch = models.CharField(verbose_name='调度', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务表'
        verbose_name_plural = verbose_name
