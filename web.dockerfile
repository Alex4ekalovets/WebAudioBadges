FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Omsk /etc/localtime && \
    echo "Asia/Omsk" > /etc/timezone

COPY web/requirements.txt ./

RUN pip install -r requirements.txt

COPY web ./web

ENV PYTHONPATH=/app
