try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from .parser import Parser


class NmapHTTPScanParser(Parser):
    """nmap -sV -sC -p 80,443,7000,8080 -iL {input} --open -oX {output_file}
       for nmap 7.7.0"""

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        for host in root.findall('host'):
            hostname = host.find('hostnames').find('hostname[@type="user"]').get('name')
            for port in host.find('ports').findall('port'):
                port_id = port.get('portid')
                server = port.find('service').get('product')
                title = port.find('script[@id="http-title"]').get('output')
                self.add_record('{}:{}:{}:{}'.format(hostname, port_id, server, title))
