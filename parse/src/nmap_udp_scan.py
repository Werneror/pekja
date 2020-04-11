try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from .parser import Parser


class NmapUdpScanParser(Parser):
    """nmap -sU -p- -iL {input} -oX {output_file} --open
       for nmap 7.7.0"""

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        for host in root.findall('host'):
            ipv4 = host.findall("address[@addrtype='ipv4']")[0].get('addr')
            for port in host.findall(".//port"):
                record = '{}:{}'.format(ipv4, port.get('portid'))
                self.add_record(record)
