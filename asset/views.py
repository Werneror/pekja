from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Record


@login_required(login_url='/admin')
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
