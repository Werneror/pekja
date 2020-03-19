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
