from django.db import models


class Project(models.Model):

    name = models.CharField(verbose_name='项目名', max_length=100)
    src_link = models.URLField(verbose_name='SRC链接', null=True, blank=True)
    comment = models.TextField(verbose_name='备注', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name


class Record(models.Model):

    record = models.CharField(verbose_name='记录', max_length=200)
    project = models.ForeignKey(verbose_name='项目', to=Project, on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
    type = models.CharField(verbose_name='类型', max_length=50, null=True, blank=True)
    source = models.CharField(verbose_name='来源', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.record

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name
