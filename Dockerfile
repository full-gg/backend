FROM python:3.8

COPY . /app

EXPOSE 6969

WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT python /app/main.py
