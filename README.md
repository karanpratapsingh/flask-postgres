# Flask application

## Run the app

```
$ make dev
```

## See database

Open table plus and connect with host as `localhost` and creds from `.env`

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
