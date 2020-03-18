from .parser import Parser


class CTFRParser(Parser):
    """python3 ctfr.py -d facebook.com -o /home/shei/subdomains_fb.txt
       for ctfr 86a804a"""

    def parse(self):
        with open(self.file_path) as f:
            for line in f:
                domain = line.strip()
                self.add_record(domain)
