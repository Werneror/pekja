from import_export import fields
from import_export import resources
from import_export.widgets import BooleanWidget
from import_export.widgets import ForeignKeyWidget

from pekja.widgets import ChoicesWidget
from asset.models import Project
from .models import Tool
from .models import Task


class ToolResource(resources.ModelResource):

    id = fields.Field(column_name='ID', attribute='id')
    name = fields.Field(column_name='工具名', attribute='name')
    link = fields.Field(column_name='项目地址', attribute='link')
    type = fields.Field(column_name='记录类型', attribute='type')
    parse_class_name = fields.Field(column_name='解析类名', attribute='parse_class_name')
    command = fields.Field(column_name='调用命令', attribute='command')
    input_type = fields.Field(column_name='输入参数类型', attribute='input_type',
                              widget=ChoicesWidget(Tool.input_type_choices))
    version = fields.Field(column_name='版本', attribute='version')
    comment = fields.Field(column_name='备注', attribute='comment')

    class Meta:
        model = Tool


class TaskResource(resources.ModelResource):

    id = fields.Field(column_name='ID', attribute='id')
    name = fields.Field(column_name='任务名', attribute='name')
    project = fields.Field(column_name='项目', attribute='project', widget=ForeignKeyWidget(Project, 'name'))
    tool = fields.Field(column_name='工具', attribute='tool', widget=ForeignKeyWidget(Tool, 'name'))
    input = fields.Field(column_name='输入', attribute='input')
    dispatch = fields.Field(column_name='调度', attribute='dispatch')
    active = fields.Field(column_name='是否生效', attribute='active', widget=BooleanWidget())

    class Meta:
        model = Task

