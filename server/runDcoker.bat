docker pull mongo

docker stop node-mongoose
docker container rm node-mongoose

docker run --name node-mongoose -d -p 27017:27017 mongo
