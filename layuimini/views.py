# coding:utf-8
import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin

from asset.models import Record
from asset.models import Project
from task.models import Tool
from task.models import Task
from task.models import BatchTask


@login_required(login_url='/login/')
def timeline(request):
    try:
        page = int(request.GET.get('page', default=1))
    except ValueError:
        page = 1
    try:
        limit = int(request.GET.get('limit', default=10))
    except ValueError:
        limit = 10
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
        'disabled_next_page': True if page*limit > len(records) else False,
        'next_page': page+1,
        'project': project,
    }
    return render(request, 'timeline.html', context)


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
    print(request.POST)
    try:
        page = int(request.GET.get('page', default=1))
    except ValueError:
        page = 1
    try:
        limit = int(request.GET.get('limit', default=10))
    except ValueError:
        limit = 10
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
        'disabled_next_page': True if page*limit > len(records) else False,
        'next_page': page+1,
        'project': project,
    }
    return render(request, 'page/timeline.html', context)
