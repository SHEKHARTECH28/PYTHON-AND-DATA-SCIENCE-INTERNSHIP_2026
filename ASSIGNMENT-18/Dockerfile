FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    default-jdk \
    wget \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

RUN pip install --no-cache-dir pyspark==3.5.1

WORKDIR /app

COPY . .

CMD ["python", "app.py"]