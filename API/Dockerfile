FROM python:3.9.0-slim-buster

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
RUN pip install --upgrade pip

WORKDIR /urs/src/worse

COPY requirements.txt ./
COPY api.py ./
RUN pip install -r ./requirements.txt

EXPOSE 49500
CMD ["python", "api.py"]