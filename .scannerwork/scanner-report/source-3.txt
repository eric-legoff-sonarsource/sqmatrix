# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.9-alpine AS builder
EXPOSE 8000
WORKDIR /opt/app
COPY requirements.txt /opt/app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /opt/app 
RUN chmod +x /opt/app/docker-entrypoint.sh
ENTRYPOINT  /opt/app/docker-entrypoint.sh