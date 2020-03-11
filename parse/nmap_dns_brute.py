try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from .parser import Parser


class NmapDnsBruteParser(Parser):
    """nmap -sn -Pn --script=dns-brute {input} -oX {output_file}
       for nmap 7.7.0"""

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        for domain in root.findall(".//*[@key='hostname']"):
            self.add_record(domain.text)
