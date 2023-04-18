## syntax=docker/dockerfile:1

## load python 3.8
FROM python:3.8

## the tutorials include these; todo- figure out what they do
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

## who doesn't love a "stuff" directory!  :)
WORKDIR /container_project_stuff/x_project_code
RUN mkdir /container_project_stuff/logs
RUN mkdir /container_project_stuff/DBs

## set up the python environment
COPY . /container_project_stuff/x_project_code/
RUN pip install -r ./config/requirements_localdev.txt 
