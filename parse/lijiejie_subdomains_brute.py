# coding: utf-8
from .parser import Parser


class LijiejieSubDomainsBrute(Parser):
    """/usr/local/bin/python2 /opt/subDomainsBrute/subDomainsBrute.py --full -o {output_file} {input}
       for https://github.com/lijiejie/subDomainsBrute bac5eb3"""

    def parse(self):
        with open(self.file_path) as f:
            for line in f:
                domain = line.split('\t')[0].strip()
                if domain:
                    self.add_record(domain)
