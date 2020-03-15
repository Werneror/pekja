import json

from .parser import Parser


class CensysEnumerationEmail(Parser):
    """python censys_enumeration.py --outfile {output_file} {input}
       for censys_enumeration.py 10d42fa3"""

    def parse(self):
        with open(self.file_path) as f:
            output = json.loads(f.read())
        for domain in output:
            sub_domains = domain.get('emails', list())
            for sub_domain in sub_domains:
                self.add_record(sub_domain)
