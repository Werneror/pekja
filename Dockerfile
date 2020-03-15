FROM python:3.6

RUN apt-get update && apt-get upgrade -y
RUN pip install -U pip setuptools

RUN mkdir -p /opt/pekja
COPY . /opt/pekja
RUN pip install -r /opt/pekja/requirements.txt

WORKDIR /opt/pekja
EXPOSE 8000

ENTRYPOINT ["/opt/pekja/start.sh"]
