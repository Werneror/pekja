import os
from html import escape
from platform import system

from crontab import CronTab

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from pekja.settings import DEFAULT_FROM_EMAIL
from pekja.settings import DATA_DIRS
from pekja.settings import CRON_USER
from task.models import Task


def get_input_file_path(obj):
    return os.path.join(DATA_DIRS, 'input-{}.txt'.format(obj.id))


def get_output_file_path(obj):
    return os.path.join(DATA_DIRS, 'output-{}.txt'.format(obj.id))


def get_mail_report_dispatch_file_path():
    return os.path.join(DATA_DIRS, 'mail_report_dispatch.txt')


def get_task_cron_comment(obj):
    return 'task-{}-pekja'.format(obj.id)


def get_batch_task_cron_comment(obj):
    return 'batch-task-{}-pekja'.format(obj.id)


def get_mail_report_cron_comment():
    return '#send-mail-report-pekja'


def get_windows_cron_file_path():
    cron_file_path = os.path.join(DATA_DIRS, 'windows_crontab.txt')
    if not os.path.exists(cron_file_path):
        with open(cron_file_path, 'w') as f:
            pass
    return cron_file_path


def get_task_by_id(task_id):
    """
    根据ID返回Task
    :param task_id:
    :return:
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None
    else:
        return task


def get_user_emails():
    """
    获取所有用户的邮箱地址
    :return:
    """
    user = get_user_model()
    emails = [email for email in user.objects.values_list('email', flat=True) if email != '']
    return emails


def send_mail_to_users(subject, title, message):
    """
    给所有用户发送邮件
    :param subject:
    :param title:
    :param message:
    :return:
    """
    emails = get_user_emails()
    if len(emails) > 0:
        msg_html = render_to_string('email.html', {'title': title, 'content': message})
        msg = EmailMessage(subject=subject, body=msg_html, from_email=DEFAULT_FROM_EMAIL, to=emails)
        msg.content_subtype = 'html'
        return msg.send()


def rowspan_html_table(headers, input_dict):
    """
    将输入的字典转换为HTML表格
    :param headers:
    :param input_dict:
    :return:
    """
    table = '<table border="1" cellspacing="0"><thead><tr>'
    for header in headers:
        table += '<th style="text-align: center;">' + escape(header) + '</th>'
    table += '</tr></thead>'
    for key in input_dict:
        for index, sub_key in enumerate(input_dict[key]):
            row = '<tr>'
            if index == 0:
                row += '<td rowspan="{}" style="text-align: center;">'.format(len(input_dict[key])) + key + '</td>'
            row += '<td style="text-align: center;">' + escape(sub_key) + '</td>'
            row += '<td style="text-align: center;">' + escape(str(input_dict[key][sub_key])) + '</td>'
            row += '</tr>'
            table += row
    table += '</table>'
    return table


def open_crontab():
    """
    打开crontab
    :return:
    """
    if system() == 'Windows':
        cron = CronTab(tabfile=get_windows_cron_file_path())  # 仅用于调试
    else:
        cron = CronTab(user=CRON_USER)
    return cron


def human_size(size):
    def str_of_size(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return str_of_size(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = str_of_size(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return '{}.{:>02d} {}'.format(integer, remainder, units[level])
