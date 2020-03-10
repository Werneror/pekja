import os

from pekja.settings import DATA_DIRS


def get_input_file_path(obj):
    return os.path.join(DATA_DIRS, 'input-{}.txt'.format(obj.id))


def get_output_file_path(obj):
    return os.path.join(DATA_DIRS, 'output-{}.txt'.format(obj.id))


def get_task_cron_comment(obj):
    return 'task-{}-pekja'.format(obj.id)


def get_windows_cron_file_path():
    cron_file_path = os.path.join(DATA_DIRS, 'windows_crontab.txt')
    if not os.path.exists(cron_file_path):
        with open(cron_file_path, 'w') as f:
            pass
    return cron_file_path
