from django.core.exceptions import ValidationError
from crontab import CronSlices


def cron_validator(value):
    """
    校验是否是有效的Cron表达式
    :param value:
    :return:
    """
    if not CronSlices.is_valid(value):
        raise ValidationError('不是有效的Cron表达式')


def command_validator(value):
    """
    校验命令中是否包含输入文件和输出文件占位符
    :param value:
    :return:
    """
    if '{input}' not in value or '{output_file}' not in value:
        raise ValidationError('命令中必须包含输入占位符`{input}`和输出文件占位符`{output_file}`')
