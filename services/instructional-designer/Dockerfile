FROM apache/spark:4.0.0 

USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["/opt/spark/bin/spark-submit", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0", \
     "--master", "spark://spark-master:7077", \
     "--conf", "spark.cores.max=1", \
     "--conf", "spark.executor.cores=1", \
     "/app/driver.py"]