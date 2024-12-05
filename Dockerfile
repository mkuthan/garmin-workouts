FROM python:3.13.1-slim-bookworm

ARG PLATFORM

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt && rm -rf /root/.cache/pip

COPY . .

CMD ["python", "-u", "bot.py"]