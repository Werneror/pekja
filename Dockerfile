FROM python:3.6

# Update
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y
RUN pip install -U pip setuptools
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install pekja
RUN mkdir -p /opt/pekja
COPY . /opt/pekja
RUN pip install -r /opt/pekja/requirements.txt

# Install tool: nmap 7.70
RUN apt-get install -y nmap=7.70+dfsg1-6

# Run pekja
WORKDIR /opt/pekja
EXPOSE 8000
ENTRYPOINT ["/opt/pekja/start.sh"]
