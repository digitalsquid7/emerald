# Emerald

Emerald generates and sends emails

## Setup a MySQL Docker container

Official MySQL Docker resource: https://hub.docker.com/_/mysql \
Helpful MySQL Docker resource: https://earthly.dev/blog/docker-mysql/

### Create the database

```bash
docker run --name test-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=emerald --network=bridge -d -p 3306:3306 mysql:latest
```

- `--name test-mysql` name of the docker container
- `-e MYSQL_ROOT_PASSWORD=my-secret-pw` set environment variables
- `-d` run as a background process
- `-p 3306:3306` forward the port so the DB can be connected to outside the container (from localhost)
- `mysql:latest` use the latest version of the official MySQL image 

### Connect to the database

```bash
docker exec -it test-mysql mysql -p
```

### Test email server

```bash
python -m smtpd -c DebuggingServer -n 127.0.0.1:1025
```

### Design logo

https://www.adobe.com/express/create/logo

### Taskfile
https://taskfile.dev/