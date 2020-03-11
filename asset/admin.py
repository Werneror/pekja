from django.contrib import admin
from django.utils.html import format_html
from django.utils.html import escape

from import_export.admin import ImportExportActionModelAdmin

from .models import Project
from .models import Record
from .resources import ProjectResource
from .resources import RecordResource


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


admin.site.site_header = 'Pekja'
