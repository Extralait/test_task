# Graphite

### Project run
```
docker build -t web-image Back
docker-compose up
```
### Project update
```
docker-compose up -d --build
docker-compose down
```

### Run script
```
docker-compose exec web {script} 
```

### Swarm
```
docker swarm init --advertise-addr 127.0.0.1:2377
docker stack deploy -c docker-compose.yml  proj
```  
### Remove swarm 
```
docker stack rm proj
docker swarm leave --force
```

