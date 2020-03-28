# TODO: update python to 3.8
FROM python:3.6-stretch

USER root
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "tail", "-f", "/dev/null" ]
# CMD ["sh", "-c", "locust -f $FILE --no-web -c $USER_NUMBER -r $SPAWN_RATE -t $TIME --only-summary"]
