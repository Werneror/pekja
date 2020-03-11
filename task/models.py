from django.db import models

from asset.models import Project
from .validators import cron_validator
from .validators import command_validator


class Tool(models.Model):

    INPUT_TYPE_FILE = 'file'
    INPUT_TYPE_PARAMETER = 'parameter'
    input_type_choices = ((INPUT_TYPE_FILE, '文件'),
                          (INPUT_TYPE_PARAMETER, '参数'))

    name = models.CharField(verbose_name='工具名', max_length=100)
    link = models.URLField(verbose_name='项目地址', null=True, blank=True)
    type = models.CharField(verbose_name='记录类型', max_length=50)
    parse_class_name = models.CharField(verbose_name='输出解析类', max_length=50)
    command = models.CharField(verbose_name='调用命令', max_length=500, validators=[command_validator])
    input_type = models.CharField(verbose_name='输入参数类型', max_length=50,
                                  choices=input_type_choices, default=INPUT_TYPE_FILE)
    comment = models.CharField(verbose_name='备注', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工具表'
        verbose_name_plural = verbose_name


class Task(models.Model):

    INPUT_FILE_TYPE_STATIC = 'static_file'
    INPUT_FILE_TYPE_DYNAMIC = 'dynamic_file'
    input_file_type_choices = ((INPUT_FILE_TYPE_STATIC, '静态'),
                               (INPUT_FILE_TYPE_DYNAMIC, '动态'))
    name = models.CharField(verbose_name='任务名', max_length=100)
    project = models.ForeignKey(verbose_name='所属项目', to=Project, on_delete=models.CASCADE)
    tool = models.ForeignKey(verbose_name='工具', to=Tool, on_delete=models.CASCADE)
    input = models.TextField(verbose_name='输入')
    input_file_type = models.CharField(verbose_name='输入文件类型', max_length=50,
                                       choices=input_file_type_choices, default=INPUT_FILE_TYPE_STATIC)
    dispatch = models.CharField(verbose_name='调度', max_length=100, validators=[cron_validator])
    active = models.BooleanField(verbose_name='是否生效', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务表'
        verbose_name_plural = verbose_name
