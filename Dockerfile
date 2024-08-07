FROM nvidia/cuda:12.5.1-cudnn-runtime-ubuntu20.04

# Установка дополнительных зависимостей, если нужно
ENV PYTHONUNBUFFERED=1

USER 0

WORKDIR /app

RUN apt-get update && \
    ln -sf /usr/share/zoneinfo/Asia/Omsk /etc/localtime && \
    echo "Asia/Omsk" > /etc/timezone && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.10 python3-pip python3-setuptools python3-distutils libcudnn8 libcudnn8-dev


COPY ./requirements/requirements.txt .


RUN pip install -r requirements.txt

# Копирование исходных файлов в рабочую директорию Docker-контейнера
COPY ./temp ./temp

RUN mkdir -p "/app/records"

# Команда для запуска скрипта
CMD ["python3", "/app/temp/main.py"]


