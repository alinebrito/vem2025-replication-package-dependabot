FROM --platform=linux/amd64 python:3.12.7-alpine3.20 AS build

WORKDIR /app/

COPY src/ requirements.txt gcp-credentials.json /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "run.py"]