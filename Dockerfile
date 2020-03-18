FROM python:3.6

# Update
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y
RUN pip install -U pip setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install crontab
RUN apt-get install -y cron
RUN service cron start
RUN update-rc.d cron defaults

# Install tool: nmap 7.70
RUN apt-get install -y nmap=7.70+dfsg1-6

# Install censys-enumeration
RUN mkdir -p /opt/censys_enumeration
RUN git clone https://github.com/0xbharath/censys-enumeration.git /opt/censys_enumeration
RUN pip install -r /opt/censys_enumeration/requirements.txt

# Install CTFR
RUN mkdir -p /opt/ctfr
RUN git clone https://github.com/UnaPibaGeek/ctfr.git /opt/ctfr
RUN pip3 install -r /opt/ctfr/requirements.txt

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
