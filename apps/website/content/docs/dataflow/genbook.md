```mermaid
flowchart TD
     subgraph Interazione con l'Utente
          A[App / CLI] -->|Crea Richiesta GenBook| B[Gateway API]
     end

     subgraph Nucleo del Sistema
          B -->|Genera ID Lavoro, Crea Stato GenBook| C[MongoDB]
          B -->|Pubblica Lavoro su Kafka| D[Topic Kafka: book-queue]
     end

     subgraph Pipeline di Elaborazione Kafka
          D -->|Consuma Lavoro| E[prompt-enricher]
          E -->|Espande il prompt con link| E
          E -->|Pubblica prompt arricchito| F[Topic Kafka: enriched_prompts]

          F -->|Consuma prompt arricchito| G[instructional-designer]
          G -->|Genera struttura libro e info arricchimento paragrafi| G
          G -->|Pubblica struttura libro| H[Topic Kafka: book-structure]
          G -->|Pubblica info arricchimento paragrafi| I[Topic Kafka: paragraph-enrichment]

          I -->|Consuma info arricchimento paragrafi| J[paragraph-enricher]
          J -->|Genera testo Markdown dalle info| J
          J -->|Pubblica paragrafo arricchito| K[Topic Kafka: enriched-paragraphs]
     end

     subgraph Aggregazione Finale
          H -->|Consuma struttura libro| L[book-aggregator]
          K -->|Consuma paragrafi arricchiti| L
          L -->|Aggrega e costruisce il libro finale| L
          L -->|Pubblica libro finale| M[Topic Kafka: generated-books]
          M -->|Aggiorna Stato GenBook in MongoDB| C
     end

     subgraph Archiviazione dei Dati e Logging
          C -- Stato GenBook --> X{Dati}
          subgraph Stack ELK
                E --> Z[Logstash]
                G --> Z
                J --> Z
                L --> Z
                Z --> Y[Elasticsearch]
          end
     end
```

# Documentazione del Flusso di Dati di GenBook

## Panoramica

Questo documento descrive il flusso di dati del sistema GenBook, basandosi sul diagramma del flusso di dati. Il sistema è suddiviso in quattro sezioni principali:

1. **Interazione con l'Utente**: L'utente interagisce con il sistema tramite un'applicazione o CLI, avviando la creazione di una richiesta GenBook che viene gestita dal Gateway API.
2. **Nucleo del Sistema**: Il Gateway API genera un ID lavoro unico, aggiorna lo stato in MongoDB e pubblica il lavoro su un topic Kafka per l'elaborazione.
3. **Pipeline di Elaborazione Kafka**: Una serie di microservizi elabora i dati, arricchendo i prompt, generando la struttura del libro e i paragrafi arricchiti.
4. **Aggregazione Finale e Archiviazione**: I dati vengono aggregati per costruire il libro finale, pubblicati su un topic Kafka e archiviati in MongoDB. I log vengono raccolti dallo stack ELK per il monitoraggio.

Ogni componente e processo è rappresentato nel diagramma sopra.
