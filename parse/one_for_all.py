# coding: utf-8

import json

from .parser import Parser


class OneForAllParser(Parser):
    """/usr/local/bin/python /opt/oneforall/oneforall/oneforall.py --target {input} --out {output_file} --format json run
       for OneForAll.py v0.3.0"""

    def parse(self):
        with open(self.file_path, encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                if domain:
                    self.add_record(domain)
