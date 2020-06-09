docker build . -t "iexalt/runescrape-agent" &
docker stop runescrape-agent &
docker rm runescrape-agent &
wait
docker run -d --name runescrape-agent --network=host -e RUNESCRAPE_SERVICE=localhost -e RUNESCRAPE_PORT=8000 -e RUNESCRAPE_ENDPOINT=items/history  iexalt/runescrape-agent
