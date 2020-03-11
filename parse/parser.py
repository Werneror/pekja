import os
import time
from pekja.utils import get_output_file_path
from asset.models import Record


class Parser:

    def __init__(self, task):
        self.task = task
        self.file_path = get_output_file_path(task)

    def parse(self):
        pass

    def rename_file(self):
        now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        os.rename(self.file_path,
                  self.file_path.replace('-{}.txt'.format(self.task.id), '-{}-{}.txt'.format(self.task.id, now)))

    def add_record(self, record):
        """
        添加一条记录
        :param record: 记录内容
        :return: 是否成功，错误消息
        """
        try:
            record = Record.objects.get(record=record, project=self.task.project, type=self.task.tool.type)
        except Record.DoesNotExist:
            Record(record=record, project=self.task.project, type=self.task.tool.type, source=self.task.tool.name).save()
            return True
        except Record.MultipleObjectsReturned:
            return False
        else:
            if self.task.tool.name not in record.source:
                record.source += ',' + self.task.tool.name
            record.save()    # 保存一次是为了更新最后修改时间
            return True
