import os

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from pekja.settings import DEFAULT_FROM_EMAIL
from pekja.settings import DATA_DIRS
from task.models import Task


def get_input_file_path(obj):
    return os.path.join(DATA_DIRS, 'input-{}.txt'.format(obj.id))


def get_output_file_path(obj):
    return os.path.join(DATA_DIRS, 'output-{}.txt'.format(obj.id))


def get_task_cron_comment(obj):
    return 'task-{}-pekja'.format(obj.id)


def get_batch_task_cron_comment(obj):
    return 'batch-task-{}-pekja'.format(obj.id)


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


def send_mail_to_users(subject, title, message):
    """
    给所有用户发送邮件
    :param subject:
    :param title:
    :param message:
    :return:
    """
    emails = [email for email in User.objects.values_list('email', flat=True) if email != '']
    if len(emails) > 0:
        msg_html = render_to_string('email.html', {'title': title, 'content': message})
        msg = EmailMessage(subject=subject, body=msg_html, from_email=DEFAULT_FROM_EMAIL, to=emails)
        msg.content_subtype = 'html'
        return msg.send()
