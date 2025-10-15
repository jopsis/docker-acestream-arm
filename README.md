# docker-acestream-arm

[Dockerhub](https://hub.docker.com/r/jopsis/acestream-arm)

Docker image to run acestream-engine in RaspberryPI or armv7 system.

## Quick Start with Docker Compose

The easiest way to run Acestream:

```bash
docker-compose up -d
```

To stop:
```bash
docker-compose down
```

## How to build
```
docker build -t acestream-arm .
```
If you want build image with custom configuration, uncomment the line 
```
ADD acestream.conf  /acestream.engine/
```


## How to run

### Using Docker Run

To run with default config:
```bash
docker run -d --name acestream --privileged -p 8621:8621 -p 6878:6878 jopsis/acestream:arm
```

If you want a custom configuration:
```bash
docker run -d --name acestream --privileged -v $(pwd)/acestream.conf:/acestream.engine/acestream.conf -p 8621:8621 -p 6878:6878 jopsis/acestream:arm
```

## How to play
Acestream can be played using next url
```
http://<docker_host>:6878/ace/getstream?id=<ID>
```

## Acestream Settings
```
http://<docker_host>:6878/webui/app/acestream/server#proxy-server-settings
```
