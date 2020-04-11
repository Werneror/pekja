import os

from django.test import TestCase
from entities.models import Task
from entities.models import Tool
from entities.models import Record
from entities.models import Project

from parse.sublist3r_parser import Sublist3rParser
from parse.one_for_all import OneForAllParser
from parse.lijiejie_subdomains_brute import LijiejieSubDomainsBrute
from parse.censys_enumeration_email import CensysEnumerationEmail
from parse.censys_enumeration_domain import CensysEnumerationDomain
from parse.ctfr import CTFRParser
from parse.nmap_dns_brute import NmapDnsBruteParser
from parse.nmap_syn_scan import NmapSynScanParser
from parse.nmap_udp_scan import NmapUdpScanParser


class ParserTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name='test_project')

    def test_sublist3r_parser(self):
        tool = Tool.objects.create(name='sublist3r_tool', type='sublist3r_type')
        task = Task.objects.create(name='sublist3r_task', project=self.project, tool=tool)
        parser = Sublist3rParser(task, os.path.join('parse', 'examples', 'sublist3r.txt'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='sublist3r_type').count(), 2)

    def test_censys_enumeration_domain(self):
        tool = Tool.objects.create(name='censys_enumeration_domain_tool', type='censys_enumeration_domain_type')
        task = Task.objects.create(name='censys_enumeration_domain_task', project=self.project, tool=tool)
        parser = CensysEnumerationDomain(task, os.path.join('parse', 'examples', 'censys_enumeration.json'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='censys_enumeration_domain_type').count(), 127)

    def test_censys_enumeration_email(self):
        tool = Tool.objects.create(name='censys_enumeration_email_tool', type='censys_enumeration_email_type')
        task = Task.objects.create(name='censys_enumeration_email_task', project=self.project, tool=tool)
        parser = CensysEnumerationEmail(task, os.path.join('parse', 'examples', 'censys_enumeration.json'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='censys_enumeration_email_type').count(), 5)

    def test_one_for_all(self):
        tool = Tool.objects.create(name='one_for_all_tool', type='one_for_all_type')
        task = Task.objects.create(name='one_for_all_task', project=self.project, tool=tool)
        parser = OneForAllParser(task, os.path.join('parse', 'examples', 'one_for_all.json'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='one_for_all_type').count(), 6)

    def test_lijiejie_sub_domains_brute(self):
        tool = Tool.objects.create(name='lijiejie_sub_domains_brute_tool', type='lijiejie_sub_domains_brute_type')
        task = Task.objects.create(name='lijiejie_sub_domains_brute_task', project=self.project, tool=tool)
        parser = LijiejieSubDomainsBrute(task, os.path.join('parse', 'examples', 'lijiejie_sub_domains_brute.txt'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='lijiejie_sub_domains_brute_type').count(), 4)

    def test_ctfr(self):
        tool = Tool.objects.create(name='ctfr_tool', type='ctfr_type')
        task = Task.objects.create(name='ctfr_task', project=self.project, tool=tool)
        parser = CTFRParser(task, os.path.join('parse', 'examples', 'ctfr.txt'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='ctfr_type').count(), 7)

    def test_nmap_sub_domain_brute(self):
        tool = Tool.objects.create(name='nmap_sub_domain_brute_tool', type='nmap_sub_domain_brute_type')
        task = Task.objects.create(name='nmap_sub_domain_brute_task', project=self.project, tool=tool)
        parser = NmapDnsBruteParser(task, os.path.join('parse', 'examples', 'nmap_sub_domain_brute.xml'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='nmap_sub_domain_brute_type').count(), 4)

    def test_nmap_syn_scan(self):
        tool = Tool.objects.create(name='nmap_syn_scan_tool', type='nmap_syn_scan_type')
        task = Task.objects.create(name='nmap_syn_scan_task', project=self.project, tool=tool)
        parser = NmapSynScanParser(task, os.path.join('parse', 'examples', 'nmap_syn_scan.xml'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='nmap_syn_scan_type').count(), 6)

    def test_nmap_udp_scan(self):
        tool = Tool.objects.create(name='nmap_udp_scan_tool', type='nmap_udp_scan_type')
        task = Task.objects.create(name='nmap_udp_scan_task', project=self.project, tool=tool)
        parser = NmapUdpScanParser(task, os.path.join('parse', 'examples', 'nmap_udp_scan.xml'))
        parser.parse()
        self.assertEqual(Record.objects.filter(type='nmap_udp_scan_type').count(), 2)
