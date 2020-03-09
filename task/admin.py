from django.contrib import admin
from .models import Tool
from .models import Task


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'type', 'parse_class_name', 'command']
    search_fields = ['name', 'command', 'comment']
    list_filter = ('type',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'tool', 'dispatch']
    search_fields = ['name', 'input']
    list_filter = ('project', 'tool')


admin.site.site_header = 'Pekja'
