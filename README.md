## Compose MarketData Application
### Python/Flask application

Project structure:
```
.
├── docker-compose.yaml
├── app
    ├── api
    ├── clients
    ├── config
    ├── templates
    ├── test
    ├── app_server.py
    ├── DockerFile
    └── requirements.txt
 
```

[_docker-compose.yaml_](docker-compose.yaml)
```
services: 
  web: 
    build: app 
    ports: 
      - '5000:5000'
```

## Deploy with docker-compose

```
docker-compose up -d
Creating network "getmarketdataapp_default" with the default driver
Building web
[+] Building 37.1s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                      0.1s
 . 
 .
 .
 .
 
 => [1/5] FROM docker.io/library/python:3.6-alpine@sha256:ba487a711a0df2d0bcd3769c6b2b435c327ef21f8cafd082af8f0fbdb25846  0.0s
 => CACHED [2/5] WORKDIR /app                                                                                             0.0s
 => CACHED [3/5] COPY requirements.txt /app                                                                               0.0s
 => CACHED [4/5] RUN pip3 install -r requirements.txt --no-cache-dir                                                      0.0s
 => CACHED [5/5] COPY . /app                                                                                              0.0s
 => => naming to docker.io/library/getmarketdataapp_web                                                                   0.0s

```

## Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker ps
docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                       NAMES
10e3ce7d2649   getmarketdataapp_web   "python3 app_server.…"   50 seconds ago   Up 47 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   getmarketdataapp_web_1
```

After the application starts, navigate to `http://localhost:5000` in your web browser:
```
Enter Currency Symbol - Example BTCUSDT
Order Depth (Optional)
```

Stop and remove the containers
```
$ docker-compose down
docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                       NAMES
10e3ce7d2649   getmarketdataapp_web   "python3 app_server.…"   50 seconds ago   Up 47 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   getmarketdataapp_web_1

```


