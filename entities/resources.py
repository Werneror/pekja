from import_export import fields
from import_export import resources
from import_export.widgets import DateTimeWidget
from import_export.widgets import BooleanWidget
from import_export.widgets import ForeignKeyWidget

from .widgets import ChoicesWidget
from .models import *


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


class BatchTaskResource(resources.ModelResource):

    id = fields.Field(column_name='ID', attribute='id')
    name = fields.Field(column_name='任务名', attribute='name')
    task1 = fields.Field(column_name='任务1', attribute='task1', widget=ForeignKeyWidget(Task, 'name'))
    task2 = fields.Field(column_name='任务2', attribute='task2', widget=ForeignKeyWidget(Task, 'name'))
    task3 = fields.Field(column_name='任务3', attribute='task3', widget=ForeignKeyWidget(Task, 'name'))
    task4 = fields.Field(column_name='任务4', attribute='task4', widget=ForeignKeyWidget(Task, 'name'))
    task5 = fields.Field(column_name='任务5', attribute='task5', widget=ForeignKeyWidget(Task, 'name'))
    task6 = fields.Field(column_name='任务6', attribute='task6', widget=ForeignKeyWidget(Task, 'name'))
    task7 = fields.Field(column_name='任务7', attribute='task7', widget=ForeignKeyWidget(Task, 'name'))
    task8 = fields.Field(column_name='任务8', attribute='task8', widget=ForeignKeyWidget(Task, 'name'))
    task9 = fields.Field(column_name='任务9', attribute='task9', widget=ForeignKeyWidget(Task, 'name'))
    task10 = fields.Field(column_name='任务10', attribute='task10', widget=ForeignKeyWidget(Task, 'name'))
    dispatch = fields.Field(column_name='调度', attribute='dispatch')
    active = fields.Field(column_name='是否生效', attribute='active', widget=BooleanWidget())

    class Meta:
        model = BatchTask
