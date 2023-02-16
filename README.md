# Compatibilty Matrices for SonarQube

## Prequisites

- SonarSourcer GitHub account
  (needing permission to read https://github.com/SonarSource/sonar-enterprise)
- Create a personal access token , see https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on

- define a local environment variable `SQMATRIX_TOKEN` for that token

## Create the docker container

- Building the image

```
cd app
docker build -t elegoff/sqmatrix .
```

- Optionally recreate after force deletion of existing container :

```
docker rmi --force sqmatrix-web
```

## Running the application

```
docker compose up -d
```

and then browse here: `http://localhost:8000`

## Stopping the application

either CTRL+C
or

```
docker compose down
```

## Accessing the container shell

```
docker exec -it sqmatrix-web-1 /bin/sh
```

## Using the Administrator account

Database operations are accessible via http://localhost:8000/admin

Default Administrator credentials :

- User = admin
- Password = admin
