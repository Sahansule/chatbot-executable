FROM python:3.10-slim

LABEL maintainer="sulen"

WORKDIR /app

COPY requirements.txt .
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
