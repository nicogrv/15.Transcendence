#!/bin/sh

find app/staticfiles/avatars -type f ! -name 'poda.png' -exec rm -f {} +
find app/static/avatars -type f ! -name 'poda.png' -exec rm -f {} +

docker ps -qa | xargs -r docker stop
docker ps -qa | xargs -r docker rm
docker images -qa | xargs -r docker rmi -f
docker volume ls -q | xargs -r docker volume rm
docker network ls -q --filter type=custom | xargs -r docker network rm


