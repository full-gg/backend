FROM python:3.13.7-trixie

COPY . /app

EXPOSE 6969

WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT python /app/main.py
