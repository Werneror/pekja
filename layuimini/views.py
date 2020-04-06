# coding:utf-8
import os
import time
import datetime

import psutil
from crontab import CronSlices

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponseNotFound
from django.views.decorators.clickjacking import xframe_options_sameorigin

from pekja.settings import DATA_DIRS
from pekja.utils import open_crontab
from pekja.utils import get_user_emails
from pekja.utils import human_size
from pekja.utils import get_mail_report_cron_comment
from entities.models import Record
from entities.models import Project
from entities.models import Tool
from entities.models import Task
from entities.models import BatchTask
from command.cron_task import set_cron_mail_report


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html', {'user_name': get_user(request)})


def user_login(request):
    login_failed = False
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('/')
        else:
            login_failed = True
    return render(request, 'login.html', {'login_failed': login_failed})


def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def download(request, file_name):
    if os.path.exists(os.path.join(DATA_DIRS, file_name)):
        file = open(os.path.join(DATA_DIRS, file_name), 'rb')
        return FileResponse(file)
    else:
        return HttpResponseNotFound()


@login_required(login_url='/login/')
def api_clear(request):
    return JsonResponse({'code': 1, 'msg': 'The server cleared the cache successfully'})


@login_required(login_url='/login/')
def api_graph(request):
    amount = list()
    data = dict()
    for record_type in Record.objects.values('type').distinct():
        data[record_type.get('type')] = list()
    date = datetime.datetime.now() - datetime.timedelta(days=6)
    end_date = datetime.datetime.now()
    date_list = list()
    while date <= end_date:
        date_list.append(date.strftime('%Y-%m-%d'))
        for record_type in data:
            data[record_type].append(Record.objects.filter(type=record_type, add_time__year=date.year,
                                                           add_time__month=date.month, add_time__day=date.day).count())
        amount.append(Record.objects.filter(add_time__year=date.year, add_time__month=date.month,
                                            add_time__day=date.day).count())
        date += datetime.timedelta(days=1)
    data.update({'总计': amount})
    return JsonResponse({'code': 0, 'msg': {'data': data, 'date_list': date_list}})


@login_required(login_url='/login/')
def api_input_file(request):
    task_id = request.GET.get('task_id')
    if task_id:
        return api_data_file(request, 'input-{}.'.format(task_id))
    else:
        return api_data_file(request, 'input-')


@login_required(login_url='/login/')
def api_output_file(request):
    task_id = request.GET.get('task_id')
    if task_id:
        return api_data_file(request, 'output-{}-'.format(task_id))
    else:
        return api_data_file(request, 'output-')


@login_required(login_url='/login/')
def api_data_file(request, prefix):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    data = list()
    for path, dir_list, file_list in os.walk(DATA_DIRS):
        for file_name in file_list:
            if file_name.startswith(prefix):
                size = os.path.getsize(os.path.join(path, file_name))
                modify_time = time.localtime(os.stat(os.path.join(path, file_name)).st_mtime)
                data.append({
                    'file_name': file_name,
                    'size': human_size(size),
                    'modify_time': time.strftime('%Y-%m-%d %H:%M:%S', modify_time)
                })
    return JsonResponse({'code': 0, 'msg': '', 'count': len(data), 'data': data[(page-1)*limit: page*limit]})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def dashboard(request):
    statistics = {
        'tool': Tool.objects.count(),
        'task': Task.objects.count(),
        'active_task': Task.objects.filter(active=True).count(),
        'batch_task': BatchTask.objects.count(),
        'active_batch_task': BatchTask.objects.filter(active=True).count(),
        'project': Project.objects.count(),
        'record': Record.objects.count(),
        'record_type': Record.objects.values('type').distinct().count(),
    }
    return render(request, 'page/dashboard.html', {'statistics': statistics})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def timeline(request):
    try:
        page = int(request.GET.get('page', default=1))
    except ValueError:
        page = 1
    try:
        limit = int(request.GET.get('limit', default=3))
    except ValueError:
        limit = 3
    project = request.GET.get('project', default='')
    record_type = request.GET.get('type', default='')

    if project != '':
        records = Record.objects.filter(project__name=project).order_by('-add_time')
    else:
        records = Record.objects.all().order_by('-add_time')
    if record_type != '':
        records = records.filter(type=record_type)

    _records = dict()
    for record in records:
        add_date = record.add_time.strftime('%Y-%m-%d')
        if add_date not in _records:
            _records[add_date] = list()
        _records[add_date].append(record)

    records = [{'date': key, 'contents': _records[key]} for key in _records]
    context = {
        'records': records[(page-1)*limit: page*limit],
        'disabled_pre_page': True if page == 1 else False,
        'pre_page': page-1,
        'disabled_next_page': True if page*limit >= len(records) else False,
        'next_page': page+1,
        'project': project,
    }
    return render(request, 'page/timeline.html', context)


@login_required(login_url='/login/')
@xframe_options_sameorigin
def crontab(request):
    jobs = list()
    for job in open_crontab():
        jobs.append(job.__str__())
    return render(request, 'page/show_code.html', {'code': '\n'.join(jobs), 'title': 'Crontab',
                                                   'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def email_report(request):
    error_msg = str()
    dispatch = str()
    if request.method == 'POST':
        dispatch = request.POST.get('dispatch')
        if CronSlices.is_valid(dispatch):
            set_cron_mail_report(dispatch)
            dispatch = str()
            error_msg = '设置成功'
        else:
            error_msg = '不是有效的Crontab表达式'
    emails = get_user_emails()
    cron = open_crontab()
    jobs = list()
    for job in cron.find_comment(get_mail_report_cron_comment()):
        jobs.append(job.__str__())
    return render(request, 'page/email_report_setting.html', {'error_msg': error_msg, 'emails': emails,
                                                              'crontab': '\n'.join(jobs), 'dispatch': dispatch,
                                                              'time': datetime.datetime.now().strftime(
                                                                  '%Y-%m-%d %H:%M:%S')
                                                              })


@login_required(login_url='/login/')
@xframe_options_sameorigin
def input_file(request):
    return render(request, 'page/show_file.html', {'api_path': '/api/input_file/'})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def output_file(request):
    return render(request, 'page/show_file.html', {'api_path': '/api/output_file/'})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def var_mail(request):
    if os.path.exists(os.path.join('/var', 'mail', 'mail')):
        with open(os.path.join('/var', 'mail', 'mail')) as f:
            mail = f.read()
    else:
        mail = '/var/mail/mail不存在'
    return render(request, 'page/show_code.html', {'code': mail, 'title': '/var/mail/mail',
                                                   'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def process(request):
    processes = list()
    processes.append('{:<10} {:<10} {:<15} {:<28} {:<20} {}'.format('pid', 'ppid', 'status', 'create time', 'name', 'cmd'))
    for pid in psutil.pids():
        p = psutil.Process(pid)
        try:
            cmd = ' '.join(p.cmdline())
        except psutil.AccessDenied:
            cmd = 'No permission to get CMD commands'
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.create_time()))
        processes.append('{:<10d} {:<10d} {:<15} {:<28} {:<20} {}'.format(p.pid, p.ppid(), p.status(), create_time, p.name(), cmd))
    return render(request, 'page/show_code.html', {'code': '\n'.join(processes), 'title': '进程信息',
                                                   'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


@login_required(login_url='/login/')
@xframe_options_sameorigin
def killer(request):
    error_msg = str()
    if request.POST.get('pid'):
        try:
            pid = int(request.POST.get('pid'))
        except ValueError:
            error_msg = '进程号必须是数字'
        else:
            if pid <= 0:
                error_msg = '进程号必须是正整数'
            elif pid == 1:
                error_msg = '不能尝试结束进程号为1的进程'
            else:
                try:
                    p = psutil.Process(pid)
                except psutil.NoSuchProcess:
                    error_msg = '进程不存在'
                else:
                    p.kill()
    return render(request, 'page/killer.html', {'error_msg': error_msg})
