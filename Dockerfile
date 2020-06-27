FROM python:3.8

# Set up for localization in China. If you are not in China, please delete this part
COPY docker/sources.list /etc/apt/sources.list
RUN pip install -U pip setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Update
RUN apt-get update && apt-get upgrade -y

# Install crontab
RUN apt-get install -y cron
RUN service cron start
RUN update-rc.d cron defaults

# Clear /opt
RUN rm -rf /opt

# Install tool: nmap
RUN apt-get install -y nmap

# Install censys-enumeration
RUN mkdir -p /opt/censys_enumeration
RUN git clone https://github.com/0xbharath/censys-enumeration.git /opt/censys_enumeration
RUN pip install -r /opt/censys_enumeration/requirements.txt

# Install CTFR
RUN mkdir -p /opt/ctfr
RUN git clone https://github.com/UnaPibaGeek/ctfr.git /opt/ctfr
RUN pip install -r /opt/ctfr/requirements.txt

# Install OneForAll
RUN mkdir -p /opt/oneforall
RUN wget https://github.com/shmilylty/OneForAll/archive/v0.3.0.tar.gz -O /opt/oneforall/v0.3.0.tar.gz
RUN tar xzf /opt/oneforall/v0.3.0.tar.gz -C /opt/oneforall/
RUN mv /opt/oneforall/OneForAll-0.3.0/* /opt/oneforall
RUN rm -rf /opt/oneforall/OneForAll-0.3.0 /opt/oneforall/v0.3.0.tar.gz
RUN apt install -y python3-testresources
RUN pip install -r /opt/oneforall/requirements.txt

# Install lijiejie/subDomainsBrute
RUN mkdir -p /opt/subDomainsBrute
RUN git clone https://github.com/lijiejie/subDomainsBrute.git /opt/subDomainsBrute
RUN apt install -y python-pip
RUN python2 -m pip install dnspython gevent

# Install Sublist3r
RUN mkdir -p /opt/Sublist3r
RUN git clone https://github.com/aboul3la/Sublist3r.git /opt/Sublist3r
RUN pip install -r /opt/Sublist3r/requirements.txt

# Install pekja
RUN mkdir -p /opt/pekja
COPY requirements.txt /opt/pekja/requirements.txt
RUN pip install -r /opt/pekja/requirements.txt
COPY . /opt/pekja
RUN chmod +x /opt/pekja/docker/start.sh

# Run pekja
WORKDIR /opt/pekja
EXPOSE 8000
ENTRYPOINT ["/opt/pekja/docker/start.sh"]
