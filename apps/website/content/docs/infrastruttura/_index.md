+++
sidebar.open = true
weight = 1
+++
## Infrastruttura del Progetto

```mermaid
flowchart LR;

    %% === Componenti del Flusso ===
    api_gateway[API Gateway]
    
    subgraph "Kafka Topics"
        book_queue["book-queue"]
        enriched_prompt["enriched-prompt"]
        book_structures["book-structures"]
        paragraphs["paragraphs"]
        enriched_paragraphs["enriched-paragraphs"]
        generated_books["generated-books"]
    end

    subgraph "Microservizi"
        prompt_enricher["prompt-enricher"]
        instructional_designer["instructional-designer"]
        paragraph_enricher["paragraph-enricher"]
        book_aggregator["book-aggregator"]
        book_producer["book-producer"]
    end

    %% Stack di Logging e Monitoring
    subgraph "Monitoring & Logging"
        logstash[Logstash]
        elastic[Elasticsearch]
        kibana[Kibana]
    end

    %% === Connessioni del Flusso Principale ===
    
    %% API Gateway -> prompt-enricher
    api_gateway --> book_queue
    book_queue --> prompt_enricher
    prompt_enricher --> enriched_prompt
    
    %% instructional-designer (Split)
    enriched_prompt --> instructional_designer
    instructional_designer --> book_structures
    instructional_designer --> paragraphs
    
    %% paragraph-enricher
    paragraphs --> paragraph_enricher
    paragraph_enricher --> enriched_paragraphs
    
    %% book-aggregator (Join)
    book_structures --> book_aggregator
    enriched_paragraphs --> book_aggregator
    
    %% book-producer (Fine del flusso)
    book_aggregator --> generated_books
    generated_books --> book_producer

    %% === Connessioni verso lo Stack di Logging ===
    enriched_prompt --> logstash
    book_structures --> logstash
    enriched_paragraphs --> logstash

    %% === Connessioni interne dello Stack ELK ===
    logstash --> elastic
    elastic --> kibana
```

### Descrizione dell'Infrastruttura

L'infrastruttura del progetto è composta da tre principali sezioni:

1. **API Gateway e Kafka Topics**:
   - L'API Gateway funge da punto di ingresso per le richieste, che vengono instradate verso il topic Kafka `book-queue`.
   - I dati attraversano una serie di topic Kafka (`enriched-prompt`, `book-structures`, `paragraphs`, `enriched-paragraphs`, `generated-books`) che fungono da buffer e punti di scambio tra i microservizi.

2. **Microservizi**:
   - I microservizi sono organizzati per gestire specifiche funzionalità:
     - `prompt-enricher`: Arricchisce i prompt ricevuti.
     - `instructional-designer`: Suddivide i dati in strutture di libro e paragrafi.
     - `paragraph-enricher`: Arricchisce i paragrafi generati.
     - `book-aggregator`: Combina le strutture e i paragrafi arricchiti.
     - `book-producer`: Produce i libri finali.

3. **Monitoring & Logging**:
   - Lo stack ELK (Logstash, Elasticsearch, Kibana) è utilizzato per il monitoraggio e la registrazione dei log.
   - I dati di log vengono inviati da vari componenti a Logstash, che li inoltra a Elasticsearch per l'archiviazione. Kibana fornisce un'interfaccia per la visualizzazione.

### Flusso dei Dati

- Le richieste iniziano dall'API Gateway e vengono elaborate attraverso una pipeline di microservizi.
- I dati vengono arricchiti, suddivisi, aggregati e infine trasformati in libri generati.
- Durante il processo, i log vengono raccolti e analizzati per garantire il monitoraggio continuo.

### Architettura Modulare

L'architettura modulare consente di:

- Scalare i singoli componenti in base alle necessità.
- Semplificare la manutenzione e l'integrazione di nuove funzionalità.
- Garantire un'elaborazione efficiente e affidabile.

Questa infrastruttura è progettata per supportare un flusso di lavoro robusto e scalabile, con un'attenzione particolare al monitoraggio e alla tracciabilità dei dati.
