git pull
docker build -t pekja .
docker stop pekja
docker rm pekja
docker run -d -p 8000:8000 --env-file env -v /opt/pekja:/opt/pekja/data --restart=always --name pekja pekja:latest