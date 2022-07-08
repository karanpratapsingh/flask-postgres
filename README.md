# Flask application

## Run the app

```
$ make dev
```

## See database

Open port `localhost:8080` and login with server as `postgres` (no `host.docker.internal` as our db viewer container is in the same docker network)

## Start fresh

Made progress and don't want to start with a million migrations? Reset postgres cache and start fresh.

```
$ docker system prune
$ docker volume ls
DRIVER    VOLUME NAME
local     flask-postgres_pgdata
local     flask-postgres_redisdata 

$ docker volume rm flask-postgres_pgdata postgres_redisdata 
```

Restart the dev server with fresh postgres
```
$ make dev
```