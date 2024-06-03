FROM python:3
ADD ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
VOLUME /data
VOLUME /tmp
ENV USERNAME example
ENV PASSWORD examplePassword
ENTRYPOINT ["python", "-m", "garminworkouts", "--cookie-jar", "/tmp/.garmin-cookies.txt"] 
