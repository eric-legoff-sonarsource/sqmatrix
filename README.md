# Compatibilty Matrices for SonarQube

## Prequisites

- SonarSourcer GitHub account
  (needing permission to read https://github.com/SonarSource/sonar-enterprise)
- define an environment variable `SQMATRIX_TOKEN` for the GitHub account

## Create the docker container

- Optionally force deletion of existing container before re-creating :

```
docker rmi --force sqmatrix-web
```

- Building the image

```
cd app
docker build -t elegoff/sqmatrix .
```

## Running the application

```
docker compose up -d
```

and then browse here: `http://localhost:8000`

## Stopping the application

```
docker compose down
```

## Accessing the container

```
docker exec -it sqmatrix-web-1 /bin/sh
```

## Using the Administrator account

Database operations are accessible via http://localhost:8000/admin

Default Adnistrator credentials :

- User = admin
- Password = admin
