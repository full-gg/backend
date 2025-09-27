FROM python:3.13

COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT python /app/main.py
