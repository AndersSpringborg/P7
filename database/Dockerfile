FROM python:3.9.0-slim-buster

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
RUN pip install --upgrade pip

WORKDIR /usr/src/worse

COPY requirements.txt ./
COPY apiDB.py ./
COPY db.py ./

RUN pip install -r ./requirements.txt

EXPOSE 49502
CMD ["python", "apiDB.py"]
