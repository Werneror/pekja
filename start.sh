#!/bin/bash

python manage.py migrate --noinput
python manage.py init_admin
python manage.py is_tool_empty && python manage.py loaddata tool.json
python manage.py runserver 127.0.0.1:8000
