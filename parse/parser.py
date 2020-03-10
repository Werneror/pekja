import os
import time
from pekja.utils import get_output_file_path


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
