from import_export import fields
from import_export import resources
from import_export.widgets import DateTimeWidget
from import_export.widgets import ForeignKeyWidget

from .models import Project
from .models import Record


class ProjectResource(resources.ModelResource):

    id = fields.Field(column_name='ID', attribute='id')
    name = fields.Field(column_name='项目名', attribute='name')
    src_link = fields.Field(column_name='SRC链接', attribute='src_link')
    comment = fields.Field(column_name='备注', attribute='comment')

    class Meta:
        model = Project


class RecordResource(resources.ModelResource):

    id = fields.Field(column_name='ID', attribute='id')
    record = fields.Field(column_name='记录', attribute='record')
    project = fields.Field(column_name='项目', attribute='project', widget=ForeignKeyWidget(Project, 'name'))
    add_time = fields.Field(column_name='创建时间',
                            attribute='add_time',
                            widget=DateTimeWidget('%Y-%m-%d %H:%M:%S'))
    last_modify_time = fields.Field(column_name='最后修改时间',
                                    attribute='last_modify_time',
                                    widget=DateTimeWidget('%Y-%m-%d %H:%M:%S'))
    type = fields.Field(column_name='类型', attribute='type')
    source = fields.Field(column_name='来源', attribute='source')

    class Meta:
        model = Record

