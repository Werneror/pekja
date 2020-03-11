# pekja

SRC情报收集管理系统。

未开发完毕，敬请期待。。。

## 简介

在SRC漏洞挖掘中情报很关键，且需要进行**持续**的情报收集。那些新增的资产往往是最容易发现漏洞的资产。
所以开发了此系统用于自动持续进行情报收集，自动识别新增资产并报告。

## 操作系统兼容性

因使用到crontab故只支持Linux系统。
但在Windows中，生成了data/windows_crontab.txt，只要设法让这个文件中的定时任务运行，也可以。

## 支持的工具

- Nmap子域名爆破
- 

## 设计目标

- 可以方便灵活地调用已有的各种信息收集工具
- 具有较为完备的历史记录功能
- 可以邮件通知新增资产
- 支持按公司组织数据
- 不需要支持多用户


## 设计

- Web前端界面
- 数据存储
- 记录添加接口
- 任务调度
- 和其他工具的对接接口

假设其他工具都是基于命令行的
输入输出都通过文件进行，返回有意义的状态码（因为使用`&&`来判断命令是否执行成功）
调用格式为
项目、类型、来源、命令、输出文件、解析类
处理后会删除输出文件


## 数据表

### 项目表

- 项目名
- SRC地址（URL）
- 说明

### 记录表

- 记录
- 创建时间（自动设置）
- 最后更新时间（自动更新）
- 所属项目（外键）
- 记录类型
- 来源（来自于什么工具，多个工具有逗号分隔）

主键是记录、所属项目和记录类型，都相同时才算重复。


### 工具表

同一工具不同参数收集不同类型的情报在工具表里算不同工具

- 工具名字
- 工具地址链接（一般是Github项目链接）
- 记录类型
- 解析工具生成文件的Python类名，直接写类名，所有类都在parse文件夹中
- 工具调用的命令（系统命令，不限于Python编写，要求接受文件输入，且输出必须是一个文件，用{input_file}做占位符）
- 输入类型（命令行参数，文件）
- 备注

生成最终命令使用字符串替换而不是format，有多个占位符则都替换掉


### 任务表

- 任务名
- 项目（外键）
- 工具（外键）
- 输入
- 输入文件类型（空，静态，动态）
- 调度（字符串，cron表达式）

## 备份工具数据

导出：

```bash
python manage.py dumpdata task.tool --format=json > tool.json
```

导入：

```bash
python manage.py loaddata tool.json
```

## 运行

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata tool.json
python manage.py runserver
```

## 工作流程

1. 创建输入文件（文件名算法）
1. 设置定时任务
1. 执行定时任务，运行工具
1. 工具跑完后执行解析类，解析输出
1. 删除输出文件


任务的输入文件文件名是input-{task-id}.txt，输出文件的文件名是output-{task-id}.txt。
在创建任务时创建输入文件，保存任务时更新输入文件；
输出文件解析完毕后就会被重命名为output-{task-id}-{yyyy-MM-d-HH-mm-ss}.txt，以便调试。

所有输出文件和输入文件的路径由变量DATA_DIRS定义，默认是项目目录中data文件夹。

工具表中命令修改后所有相关任务的定时任务中的命令都会自动修改。


## 已知问题

批量导入时不走校验

## 其他问题

- 问：项目为何叫这个名字？
- 答：没有特别含义，是用[UNIQ名生成器](https://uniq.site/zh/)随机生成的。


- 问：有没有类似类似项目？
- 答：有，下文中列出来我已知的类似项目。


- 问：为何要重复造轮子？
- 答：我想写的实际上是一个可以调用任意信息收集工具的通过框架，和所有我已知的项目都有所不同。


## 类似项目

- [spiderfoot: an open source intelligence automation tool](https://github.com/smicallef/spiderfoot)
- [LangSrcCurise: SRC子域名资产监控](https://github.com/LangziFun/LangSrcCurise)
- [get_domain: 域名收集与监测](https://github.com/guimaizi/get_domain)
