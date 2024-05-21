FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt install -y wget

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt update && apt install -y ./google-chrome-stable_current_amd64.deb

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .



