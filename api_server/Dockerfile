FROM python:3.8.2-alpine3.11

RUN mkdir -p ~/api_server
WORKDIR /api_server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV FLASK_APP=api.py
ENV FLASK_ENV=development

EXPOSE 5000

# by default on 127.0.0.1:5000
CMD ["flask", "run", "--reload", "--host", "0.0.0.0"]
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]
