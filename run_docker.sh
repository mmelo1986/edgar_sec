echo killing old docker processes
docker-compose rm -fs -v

echo building docker containers
docker-compose up --build -d