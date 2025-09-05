# =================================================================
# STAGE 1: Build - Usa l'immagine ufficiale di Maven che include JDK e Maven
# =================================================================
# <-- LA CORREZIONE È QUI. Usiamo un'immagine che garantisce la presenza di Maven.
FROM maven:3.9.6-eclipse-temurin-17 AS builder

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia solo il pom.xml per sfruttare la cache di Docker
COPY pom.xml .

# Scarica tutte le dipendenze di Maven
RUN mvn dependency:go-offline

# Ora copia il resto del codice sorgente
COPY src ./src

# Compila l'applicazione e crea il "fat jar" con tutte le dipendenze
RUN mvn clean package -DskipTests

# =================================================================
# STAGE 2: Run - Usa un'immagine JRE leggera per l'esecuzione (Questa parte non cambia)
# =================================================================
FROM eclipse-temurin:17-jre-jammy

WORKDIR /app

# Copia solo il jar compilato dallo stage di build
COPY --from=builder /app/target/book-aggregator-1.0-SNAPSHOT-jar-with-dependencies.jar ./book-aggregator.jar

# Crea la directory per lo stato di Kafka Streams all'interno del container
RUN mkdir ./state

# Dichiara la directory di stato come un VOLUME per la persistenza
VOLUME /app/state

# Comando per avviare l'applicazione quando il container parte
ENTRYPOINT ["java", \
            "-Dkafka.bootstrap.servers=${KAFKA_BOOTSTRAP_SERVERS}", \
            "-Dstate.dir=/app/state", \
            "-jar", \
            "book-aggregator.jar"]