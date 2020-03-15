FROM python:3.6

# Update
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y
RUN pip install -U pip setuptools
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install tool: nmap 7.70
RUN apt-get install -y nmap=7.70+dfsg1-6

# Install pekja
RUN mkdir -p /opt/pekja
COPY requirements.txt /opt/pekja/requirements.txt
RUN pip install -r /opt/pekja/requirements.txt
COPY . /opt/pekja
RUN chmod +x /opt/pekja/start.sh

# Run pekja
WORKDIR /opt/pekja
EXPOSE 8000
ENTRYPOINT ["/opt/pekja/start.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
