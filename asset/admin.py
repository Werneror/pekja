from django.contrib import admin
from .models import Project
from .models import Record


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'src_link']
    search_fields = ['name', 'comment']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['record', 'project', 'add_time', 'last_modify_time', 'type', 'source']
    search_fields = ['record']
    list_filter = ('project', 'source')


admin.site.site_header = 'Pekja'
