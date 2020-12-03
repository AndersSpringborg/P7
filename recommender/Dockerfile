FROM python:3.9.0-slim-buster
RUN apt-get update -y && apt-get install -y python-pip python-dev
RUN pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 49501
ENTRYPOINT [ "python", "webapp.py" ]