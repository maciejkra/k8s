FROM python:3-slim-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY redis-consumer-producer.py ./redis-consumer-producer.py

CMD ["python","-u","redis-consumer-producer.py"]
