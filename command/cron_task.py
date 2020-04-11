import os
from sys import executable

from pekja.utils import get_input_file_path
from pekja.utils import get_output_file_path
from pekja.utils import get_mail_report_dispatch_file_path
from pekja.utils import get_task_cron_comment
from pekja.utils import get_batch_task_cron_comment
from pekja.utils import get_mail_report_cron_comment
from pekja.utils import open_crontab
from pekja.settings import BASE_DIR
from entities.models import Tool
from entities.models import Task
from entities.models import Record
from parse import get_parse_class


def set_cron_task(obj):
    """
    设置任务的定时任务
    :param obj: Task 模型对象
    :return:
    """
    command, comment = get_task_command(obj)
    set_crontab(obj.dispatch, command, comment, obj.active)


def set_cron_batch_task(obj):
    """
    设置批量任务的定时任务
    :param obj:
    :return:
    """
    commands = list()
    for task in obj.get_tasks():
        command, _ = get_task_command(task)
        commands.append(command)
    comment = get_batch_task_cron_comment(obj)
    if len(commands) > 0:
        set_crontab(obj.dispatch, ' && '.join(commands), comment, obj.active)


def get_task_command(task):
    """
    获取任务的命令
    :param task:
    :return: command, comment
    """
    output_file_path = get_output_file_path(task)
    task_cron_comment = get_task_cron_comment(task)

    if task.tool.input_type == Tool.INPUT_TYPE_FILE:
        if task.input_file_type == Task.INPUT_FILE_TYPE_STATIC:
            _input = update_static_input(task)
        else:
            _input = update_dynamic_input(task)
    else:
        _input = task.input

    pre_command = '{} {} update_input {}'.format(executable, os.path.join(BASE_DIR, 'manage.py'), task.id)
    tool_command = task.tool.command.replace('{input}', _input).replace('{output_file}', output_file_path)
    parse_command = '{} {} parse {}'.format(executable, os.path.join(BASE_DIR, 'manage.py'), task.id)
    if task.input_file_type == Task.INPUT_FILE_TYPE_DYNAMIC:
        command = ' && '.join([pre_command, tool_command, parse_command])
    else:
        command = ' && '.join([tool_command, parse_command])

    return command, task_cron_comment


def run_parse(task):
    """
    运行解析类解析任务输出结果
    :param task:
    :return:
    """
    parse_class = get_parse_class(task.tool.parse_class_name)
    if parse_class is None:
        print('Parse class {} does not exist'.format(task.tool.parse_class_name))
    else:
        p = parse_class(task)
        p.parse()
        p.rename_file()


def update_dynamic_input(task):
    """
    更新任务的动态输入
    :param task:
    :return:
    """
    if task.input_file_type == Task.INPUT_FILE_TYPE_DYNAMIC:
        input_file_path = get_input_file_path(task)
        with open(input_file_path, 'w') as f:
            for record in Record.objects.filter(project=task.project, type=task.input):
                f.write(record.record)
                f.write('\n')
        return input_file_path


def update_static_input(task):
    """
    更新任务的静态输入
    :param task:
    :return:
    """
    if task.input_file_type == Task.INPUT_FILE_TYPE_STATIC:
        input_file_path = get_input_file_path(task)
        with open(input_file_path, 'w', newline='') as f:
            f.write(task.input)
        return input_file_path


def set_crontab(dispatch, command, comment, active):
    """
    设置定时任务
    :param dispatch: 调度
    :param command: 命令
    :param comment: 备注，用于查找和更新命令
    :param active: 是否生效
    :return:
    """
    # 打开定时任务文件
    cron = open_crontab()
    # 删除该任务已存在的定时任务
    for job in cron.find_comment(comment):
        cron.remove(job)
    # 新建定时任务
    job = cron.new(command=command, comment=comment)
    job.setall(dispatch)
    if active:
        job.enable()
    else:
        job.enable(False)
    # 设置环境变量
    set_crontab_env(cron)
    # 保存定时任务
    cron.write()


def set_crontab_env(cron):
    """
    设置定时任务的环境变量
    :param cron
    :return:
    """
    for key in os.environ:
        cron.env[key] = os.environ[key]


def set_cron_mail_report(dispatch):
    """
    设置发送邮件报告的定时任务
    :param dispatch:
    :return:
    """
    comment = get_mail_report_cron_comment()
    command = '{} {} record_report'.format(executable, os.path.join(BASE_DIR, 'manage.py'))
    set_crontab(dispatch, command, comment, True)
    with open(get_mail_report_dispatch_file_path(), 'w') as f:
        f.write(dispatch)
