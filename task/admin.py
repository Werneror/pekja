from django.contrib import admin
from django.utils.html import format_html
from django.utils.html import escape

from import_export.admin import ImportExportActionModelAdmin

from .models import Tool
from .models import Task
from .resources import ToolResource
from .resources import TaskResource
from .forms import ToolForm
from .cron_task import set_cron_task


@admin.register(Tool)
class ToolAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'link_url', 'version', 'type', 'parse_class_name', 'command', 'input_type']
    search_fields = ['name', 'command', 'comment']
    list_filter = ('type', 'input_type')
    resource_class = ToolResource
    form = ToolForm

    def save_model(self, request, obj, form, change):
        obj.save()
        for task in obj.task_set.all():
            set_cron_task(task)

    def link_url(self, obj):
        if obj.link:
            url = obj.link.replace('"', r'%22')
            return format_html('<a href="{}" target="_blank">{}</a>'.format(url, escape(obj.link)))
        else:
            return obj.link

    link_url.short_description = '项目链接'


@admin.register(Task)
class TaskAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'project', 'tool', 'input_overview', 'dispatch', 'active']
    search_fields = ['name', 'input']
    list_filter = ('project', 'tool', 'active')
    resource_class = TaskResource

    def save_model(self, request, obj, form, change):
        obj.save()
        set_cron_task(obj)

    def input_overview(self, obj):
        if len(obj.input) > 10:
            return obj.input[:10] + '...'
        else:
            return obj.input
    input_overview.short_description = '输入'


admin.site.site_header = 'Pekja'
