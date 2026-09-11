FROM python:3.11-slim

WORKDIR /app

# Cancelador de creaciond de archivos .pyc
ENV PYTHONDONTWHRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD [unicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]