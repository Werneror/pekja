#!/bin/bash

# Start crontab
service cron start

# Set OneForAll's API
echo "censys_api_id = '$CENSYS_API_ID'" >> /opt/oneforall/oneforall/api.py
echo "censys_api_secret = '$CENSYS_API_SECRET'" >> /opt/oneforall/oneforall/api.py
echo "binaryedge_api = '$BINARYEDGE_API'" >> /opt/oneforall/oneforall/api.py
echo "chinaz_api = '$CHINAZ_API'" >> /opt/oneforall/oneforall/api.py
echo "bing_api_id = '$BING_API_ID'" >> /opt/oneforall/oneforall/api.py
echo "bing_api_key = '$BING_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "securitytrails_api = '$SECURITYTRAILS_API'" >> /opt/oneforall/oneforall/api.py
echo "fofa_api_email = '$FOFA_API_EMAIL'" >> /opt/oneforall/oneforall/api.py
echo "fofa_api_key = '$FOFA_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "google_api_key = '$GOOGLE_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "google_api_cx = '$GOOGLE_API_CX'" >> /opt/oneforall/oneforall/api.py
echo "riskiq_api_username = '$RISKIQ_API_USERNAME'" >> /opt/oneforall/oneforall/api.py
echo "riskiq_api_key = '$RISKIQ_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "shodan_api_key = '$SHODAN_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "threatbook_api_key = '$THREATBOOK_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "virustotal_api_key = '$VIRUSTOTAL_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "zoomeye_api_usermail = '$ZOOMEYE_API_USERMAIL'" >> /opt/oneforall/oneforall/api.py
echo "zoomeye_api_password = '$ZOOMEYE_API_PASSWORD'" >> /opt/oneforall/oneforall/api.py
echo "spyse_api_token = '$SPYSE_API_TOKEN'" >> /opt/oneforall/oneforall/api.py
echo "circl_api_username = '$CIRCL_API_USERNAME'" >> /opt/oneforall/oneforall/api.py
echo "circl_api_password = '$CIRCL_API_PASSWORD'" >> /opt/oneforall/oneforall/api.py
echo "dnsdb_api_key = '$DNSDB_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "ipv4info_api_key = '$IPV4INFO_API_KEY'" >> /opt/oneforall/oneforall/api.py
echo "passivedns_api_addr = '$PASSIVEDNS_API_ADDR'" >> /opt/oneforall/oneforall/api.py
echo "passivedns_api_token = '$PASSIVEDNS_API_TOKEN'" >> /opt/oneforall/oneforall/api.py
echo "github_api_user = '$GITHUB_API_USER'" >> /opt/oneforall/oneforall/api.py
echo "github_api_token = '$GITHUB_API_TOKEN'" >> /opt/oneforall/oneforall/api.py
echo "github_email = '$GITHUB_EMAIL'" >> /opt/oneforall/oneforall/api.py
echo "github_password = '$GITHUB_PASSWORD'" >> /opt/oneforall/oneforall/api.py

# Start pekja
python manage.py migrate --noinput
python manage.py init_admin
python manage.py loaddata tool.json
python manage.py cron_all_task
python manage.py runserver 0.0.0.0:8000 --noreload
