# syntax=docker/dockerfile:1
FROM python:3.10.0rc2-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt


CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]