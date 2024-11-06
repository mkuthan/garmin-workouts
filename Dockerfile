FROM python:3.13.0-slim-bookworm

ARG PLATFORM

ARG GARMIN_USERNAME
ARG GARMIN_PASSWORD
ARG vV02
ARG fmin
ARG fmax
ARG flt
ARG rFTP
ARG cFTP
ARG BOT_TOKEN

ENV GARMIN_USERNAME=$GARMIN_USERNAME
ENV GARMIN_PASSWORD=$GARMIN_PASSWORD
ENV vV02=$vV02
ENV fmin=$fmin
ENV fmax=$fmax
ENV flt=$flt
ENV rFTP=$rFTP
ENV cFTP=$cFTP
ENV BOT_TOKEN=$BOT_TOKEN

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt && rm -rf /root/.cache/pip

COPY . .

CMD [ "python", "-u", "./bot.py" ]