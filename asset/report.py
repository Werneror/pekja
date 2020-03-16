from asset.models import Record
from pekja.utils import send_mail_to_users
from pekja.utils import rowspan_html_table


def generate_new_record_report(date):
    """
    生成某天的新增记录报告
    :param date: <class 'datetime.datetime'>
    :return:
    """
    records = Record.objects.filter(add_time__year=date.year, add_time__month=date.month, add_time__day=date.day)

    data = dict()
    for record in records:
        if record.project.name not in data:
            data[record.project.name] = dict()
        if record.type not in data[record.project.name]:
            data[record.project.name][record.type] = 0
        data[record.project.name][record.type] += 1

    table_data = list()
    for project in data:
        for record_type in data[project]:
            table_data.append([project, record_type, data[project][record_type]])

    return rowspan_html_table(['Project', 'Type', 'Amount'], data)


def send_report_by_mail(date, report):
    """
    通过邮件发送报告
    :param date: <class 'datetime.datetime'>
    :param report: HTML
    :return:
    """
    title = 'The new record report of Pekja is shown in the following table.'
    send_mail_to_users('Pekja report for {}'.format(date.strftime('%Y-%m-%d')), title, report)
