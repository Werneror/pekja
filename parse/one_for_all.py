# coding: utf-8

import json

from .parser import Parser


class OneForAllParser(Parser):
    """/usr/local/bin/python /opt/oneforall/oneforall/oneforall.py --target {input} --out {output_file} --format json run
       for OneForAll.py b51236a"""

    def parse(self):
        with open(self.file_path) as f:
            output = json.loads(f.read())
        for item in output:
            reason = item.get('reason', '')
            if reason.startswith('(') and reason.endswith(')'):
                continue
            else:
                self.add_record(item.get('subdomain'))
                if item.get('port'):
                    ip_list = item.get('content')
                    for ip in ip_list.split(','):
                        self.add_record('{}:{}'.format(ip, item.get('port')), 'TCP端口')
                    if item.get('title'):
                        title = '{}:{}:{}'.format(item.get('subdomain'), item.get('port'), item.get('title'))
                        self.add_record(title, '网页标题')
