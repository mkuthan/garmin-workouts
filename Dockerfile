FROM python:3.11.5-alpine
ARG GARMIN_USERNAME
ENV GARMIN_USERNAME=$GARMIN_USERNAME

ARG GARMIN_PASSWORD
ENV GARMIN_PASSWORD=$GARMIN_PASSWORD

ARG vV02
ENV vV02=$vV02

ARG fmin
ENV fmin=$fmin

ARG fmax
ENV fmax=$fmax

ARG flt
ENV flt=$flt

ARG rFTP
ENV rFTP=$rFTP

ARG cFTP
ENV cFTP=$cFTP

ARG BOT_TOKEN
ENV BOT_TOKEN=$BOT_TOKEN

WORKDIR /usr/src/app

RUN apk update && apk upgrade && apk add gcc g++
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY . .

CMD [ "python", "-u", "./bot.py" ]