# Parti dalla stessa immagine base del master
FROM apache/spark:4.0.0

# Come utente root, installa pip se non presente
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
