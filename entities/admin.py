from django.contrib import admin
from django.utils.html import format_html
from django.utils.html import escape

from import_export.admin import ImportExportActionModelAdmin

from command.cron_task import set_cron_task
from command.cron_task import set_cron_batch_task
from .forms import ToolForm
from .resources import *


@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'src_link_url']
    search_fields = ['name', 'comment']
    resource_class = ProjectResource

    def src_link_url(self, obj):
        if obj.src_link:
            url = obj.src_link.replace('"', r'%22')
            return format_html('<a href="{}" target="_blank">{}</a>'.format(url, escape(obj.src_link)))
        else:
            return obj.src_link

    src_link_url.short_description = 'SRC链接'


@admin.register(Record)
class RecordAdmin(ImportExportActionModelAdmin):
    list_display = ['record', 'project', 'add_time', 'last_modify_time', 'type', 'source']
    search_fields = ['record', 'source']
    list_filter = ('project', 'type', 'source')
    resource_class = RecordResource


@admin.register(Tool)
class ToolAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'link_url', 'version', 'type', 'parse_class_name', 'command', 'input_type', 'comment']
    search_fields = ['name', 'command', 'comment']
    list_filter = ('type', 'input_type')
    resource_class = ToolResource
    form = ToolForm

    def save_model(self, request, obj, form, change):
        obj.save()
        for task in obj.task_set.all():
            set_cron_task(task)
            for i in range(1, BatchTask.MAX_TASK_AMOUNT + 1):
                for batch_task in getattr(task, 'task{}'.format(i)).all():
                    set_cron_batch_task(batch_task)

    def link_url(self, obj):
        if obj.link:
            url = obj.link.replace('"', r'%22')
            return format_html('<a href="{}" target="_blank">{}</a>'.format(url, escape(obj.link)))
        else:
            return obj.link

    link_url.short_description = '项目链接'


@admin.register(Task)
class TaskAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'project', 'tool', 'input_overview', 'dispatch', 'active']
    search_fields = ['name', 'input']
    list_filter = ('project', 'tool', 'active')
    resource_class = TaskResource

    def save_model(self, request, obj, form, change):
        obj.save()
        set_cron_task(obj)
        for i in range(1, BatchTask.MAX_TASK_AMOUNT+1):
            for batch_task in getattr(obj, 'task{}'.format(i)).all():
                set_cron_batch_task(batch_task)

    def input_overview(self, obj):
        if len(obj.input) > 20:
            return obj.input[:20] + '...'
        else:
            return obj.input
    input_overview.short_description = '输入'


@admin.register(BatchTask)
class BatchTaskAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'name', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9',
                    'task10', 'dispatch', 'active']
    search_fields = ['name']
    list_filter = ('active', )
    resource_class = BatchTaskResource

    def save_model(self, request, obj, form, change):
        obj.save()
        set_cron_batch_task(obj)


admin.site.site_header = 'Pekja'
