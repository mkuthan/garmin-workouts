FROM python:3.11.4-slim-bookworm

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y gcc g++
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]