## syntax=docker/dockerfile:1

## python 3.9x needed due to an error in 3.10 I didn't log
FROM python:3.9

## the tutorials include these; todo- figure out what they do
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

## who doesn't love a "stuff" directory!  :)
# WORKDIR /django_template_4p2_stuff/code
WORKDIR /container_project_stuff/x_project_code
RUN mkdir /container_project_stuff/logs
RUN mkdir /container_project_stuff/DBs

## set up the python environment
# COPY ./config/requirements.txt /django_template_4p2_stuff/code/
COPY ./config/requirements.txt /container_project_stuff/x_project_code/
# RUN pip install -r ./requirements.txt
RUN pip install -r ./requirements_localdev.txt