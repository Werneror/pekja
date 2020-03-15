#!/bin/bash

python manage.py migrate --noinput
python manage.py init_admin
python manage.py is_tool_empty && python manage.py loaddata tool.json
