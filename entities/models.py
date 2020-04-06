from django.db import models
from .validators import command_validator
from .validators import cron_validator


class Project(models.Model):

    name = models.CharField(verbose_name='项目名', max_length=100, unique=True)
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


class Tool(models.Model):

    INPUT_TYPE_FILE = 'file'
    INPUT_TYPE_PARAMETER = 'parameter'
    input_type_choices = ((INPUT_TYPE_FILE, '文件'),
                          (INPUT_TYPE_PARAMETER, '参数'))

    name = models.CharField(verbose_name='工具名', max_length=100, unique=True)
    link = models.URLField(verbose_name='项目地址', null=True, blank=True)
    type = models.CharField(verbose_name='记录类型', max_length=50)
    parse_class_name = models.CharField(verbose_name='输出解析类', max_length=50)
    command = models.CharField(verbose_name='调用命令', max_length=500, validators=[command_validator])
    input_type = models.CharField(verbose_name='输入参数类型', max_length=50,
                                  choices=input_type_choices, default=INPUT_TYPE_FILE)
    version = models.CharField(verbose_name='版本', max_length=50, null=True, blank=True)
    comment = models.CharField(verbose_name='备注', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工具'
        verbose_name_plural = verbose_name


class Task(models.Model):

    INPUT_FILE_TYPE_STATIC = 'static_file'
    INPUT_FILE_TYPE_DYNAMIC = 'dynamic_file'
    input_file_type_choices = ((INPUT_FILE_TYPE_STATIC, '静态'),
                               (INPUT_FILE_TYPE_DYNAMIC, '动态'))
    name = models.CharField(verbose_name='任务名', max_length=100, unique=True)
    project = models.ForeignKey(verbose_name='所属项目', to=Project, on_delete=models.CASCADE)
    tool = models.ForeignKey(verbose_name='工具', to=Tool, on_delete=models.CASCADE)
    input = models.TextField(verbose_name='输入')
    input_file_type = models.CharField(verbose_name='输入文件类型', max_length=50,
                                       choices=input_file_type_choices, default=INPUT_FILE_TYPE_STATIC)
    dispatch = models.CharField(verbose_name='调度', max_length=100, validators=[cron_validator])
    active = models.BooleanField(verbose_name='是否生效', default=True)

    def __str__(self):
        return '{}-{}'.format(self.project.name, self.name)

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name


class BatchTask(models.Model):

    name = models.CharField(verbose_name='批量任务名', max_length=100, unique=True)
    task1 = models.ForeignKey(verbose_name='任务1', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task1')
    task2 = models.ForeignKey(verbose_name='任务2', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task2')
    task3 = models.ForeignKey(verbose_name='任务3', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task3')
    task4 = models.ForeignKey(verbose_name='任务4', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task4')
    task5 = models.ForeignKey(verbose_name='任务5', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task5')
    task6 = models.ForeignKey(verbose_name='任务6', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task6')
    task7 = models.ForeignKey(verbose_name='任务7', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task7')
    task8 = models.ForeignKey(verbose_name='任务8', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task8')
    task9 = models.ForeignKey(verbose_name='任务9', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task9')
    task10 = models.ForeignKey(verbose_name='任务10', to=Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='task10')
    dispatch = models.CharField(verbose_name='调度', max_length=100, validators=[cron_validator])
    active = models.BooleanField(verbose_name='是否生效', default=True)

    MAX_TASK_AMOUNT = 10

    def get_tasks(self):
        tasks = list()
        for i in range(1, self.MAX_TASK_AMOUNT+1):
            if getattr(self, 'task{}'.format(i)) is not None:
                tasks.append(getattr(self, 'task{}'.format(i)))
        return tasks

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '批量任务'
        verbose_name_plural = verbose_name
