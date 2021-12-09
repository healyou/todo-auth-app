https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-with-docker/

export MONGODB_VERSION=5.0
curl -O --remote-name-all https://raw.githubusercontent.com/docker-library/mongo/master/$MONGODB_VERSION/{Dockerfile,docker-entrypoint.sh}

export DOCKER_USERNAME=healyou
chmod 755 ./docker-entrypoint.sh
docker build --build-arg MONGO_PACKAGE=mongodb-enterprise --build-arg MONGO_REPO=repo.mongodb.com -t $DOCKER_USERNAME/mongo-enterprise:$MONGODB_VERSION .

docker run --name mymongo -itd $DOCKER_USERNAME/mongo-enterprise:$MONGODB_VERSION
docker exec -it mymongo /usr/bin/mongo --eval "db.version()"

docker run --name mongodb -p 27017:27017 -itd healyou/mongo-enterprise:5.0
docker-compose up
