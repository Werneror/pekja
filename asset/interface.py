import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pekja.settings')
django.setup()

from asset.models import Record
from asset.models import Project


def add_record(record, project, record_type, source):
    """
    添加一条记录
    :param record: 记录内容
    :param project: 所属项目名
    :param record_type: 记录类型
    :param source: 来源
    :return: 是否成功，错误消息
    """
    try:
        project = Project.objects.get(name=project)
        Record(record=record, project=project, type=record_type, source=source).save()
    except BaseException as error:
        return False, error
    else:
        return True, str()


if __name__ == '__main__':
    add_record('test', 'a', 'email', 'test')
