#!/usr/bin/env python3
# encoding: utf-8
"""
这个脚本用于自动安装 pekja。其原理是解析 Dockerfile 文件，按 Dockerfile 文件的内容安装 pekja。
目前只支持 COPY 和 RUN 两条指令
"""

import os
from sys import version_info


def get_dockerfile_path():
    dockerfile_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'Dockerfile')
    if not os.path.exists(dockerfile_path):
        raise RuntimeError("Can't find Dockerfile in {}".format(dockerfile_path))
    return dockerfile_path


def run_docker_file(dockerfile_path):
    with open(dockerfile_path, 'r') as f:
        for line in f.readlines():
            print('[*] {}'.format(line.strip()))
            if line.startswith('COPY '):
                cmdline = 'cp ' + line[5:]
                print('[+] {}'.format(cmdline))
                os.system(cmdline)
            elif line.endswith('RUN '):
                cmdline = line[4:]
                print('[+] {}'.format(cmdline))
                os.system(cmdline)
            else:
                print('[-] skip')


def check_environment():
    if os.getuid() != 0:
        raise RuntimeError('Must run as root')
    if version_info.major != 3 or version_info.minor != 8:
        raise RuntimeError('Must run by Python 3.8')


if __name__ == '__main__':
    check_environment()
    run_docker_file(get_dockerfile_path())
