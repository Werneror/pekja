import os
from sys import executable
from platform import system

from crontab import CronTab

from pekja.utils import get_input_file_path
from pekja.utils import get_output_file_path
from pekja.utils import get_task_cron_comment
from pekja.utils import get_windows_cron_file_path
from pekja.settings import CRON_USER
from pekja.settings import BASE_DIR
from task.models import Tool
from task.models import Task
from asset.models import Record
import parse


def set_cron_task(obj):
    """
    设置定时任务
    :param obj: Task 模型对象
    :return:
    """
    input_file_path = get_input_file_path(obj)
    output_file_path = get_output_file_path(obj)
    task_cron_comment = get_task_cron_comment(obj)

    if obj.tool.input_type == Tool.INPUT_TYPE_FILE:
        if obj.input_file_type == Task.INPUT_FILE_TYPE_STATIC:
            # 更新任务输入文件
            with open(input_file_path, 'w', newline='') as f:
                f.write(obj.input)
        _input = input_file_path
    else:
        _input = obj.input

    # 生成调用工具的命令
    pre_command = '{} {} update_input {}'.format(executable, os.path.join(BASE_DIR, 'manage.py'), obj.id)
    tool_command = obj.tool.command.replace('{input}', _input).replace('{output_file}', output_file_path)
    parse_command = '{} {} parse {}'.format(executable, os.path.join(BASE_DIR, 'manage.py'), obj.id)
    if obj.input_file_type == Task.INPUT_FILE_TYPE_DYNAMIC:
        command = ' && '.join([pre_command, tool_command, parse_command])
    else:
        command = ' && '.join([tool_command, parse_command])

    # 打开定时任务文件
    if system() == 'Windows':
        cron = CronTab(tabfile=get_windows_cron_file_path())    # 仅用于调试
    else:
        cron = CronTab(user=CRON_USER)

    # 删除该任务已存在的定时任务
    for job in cron.find_comment(task_cron_comment):
        cron.remove(job)
    # 新建定时任务
    job = cron.new(command=command, comment=task_cron_comment)
    job.setall(obj.dispatch)
    if obj.active:
        job.enable()
    else:
        job.enable(False)
    # 保存定时任务
    cron.write()


def run_parse(task):
    """
    运行解析类解析任务输出结果
    :param task:
    :return:
    """
    try:
        parse_class = getattr(parse, task.tool.parse_class_name)
    except AttributeError:
        print('Parse class {} does not exist'.format(task.tool.parse_class_name))
    else:
        p = parse_class(task)
        p.parse()
        p.rename_file()


def update_input(task):
    """
    更新任务的输入
    :param task:
    :return:
    """
    if task.input_file_type == Task.INPUT_FILE_TYPE_DYNAMIC:
        input_file_path = get_input_file_path(task)
        with open(input_file_path, 'w') as f:
            for record in Record.objects.filter(project=task.project, type=task.input):
                f.write(record.record)
                f.write('\n')
