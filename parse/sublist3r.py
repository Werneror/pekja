# coding: utf-8
from .parser import Parser


class Sublist3rParser(Parser):
    """/usr/local/bin/python /opt/Sublist3r/sublist3r.py -d {input} -o {output_file}
       for https://github.com/aboul3la/Sublist3r 61ebf36"""

    def parse(self):
        with open(self.file_path) as f:
            for line in f:
                domain = line.strip()
                if domain:
                    self.add_record(domain)
