# Generated by Django 3.0.4 on 2020-03-09 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asset', '0002_record_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='工具名称')),
                ('link', models.URLField(blank=True, null=True, verbose_name='项目链接')),
                ('type', models.CharField(max_length=50, verbose_name='记录类型')),
                ('parse_class_name', models.CharField(max_length=50, verbose_name='解析类名')),
                ('command', models.CharField(max_length=500, verbose_name='调用命令')),
                ('comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '工具表',
                'verbose_name_plural': '工具表',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='任务名')),
                ('input', models.TextField(verbose_name='输入')),
                ('dispatch', models.CharField(max_length=100, verbose_name='调度')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Project', verbose_name='所属项目')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Tool', verbose_name='工具')),
            ],
            options={
                'verbose_name': '任务表',
                'verbose_name_plural': '任务表',
            },
        ),
    ]
