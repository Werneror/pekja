FROM python:3.6

# Update
RUN apt-get update && apt-get upgrade -y
RUN pip install -U pip setuptools

# Install pekja
RUN mkdir -p /opt/pekja
COPY . /opt/pekja
RUN pip install -r /opt/pekja/requirements.txt

# Install tool: nmap 7.7.0
RUN apt-get install nmap=7.7.0

# Run pekja
WORKDIR /opt/pekja
EXPOSE 8000
ENTRYPOINT ["/opt/pekja/start.sh"]
