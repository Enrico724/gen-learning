+++
weight = 1
+++


## Flusso Dati

```mermaid
graph LR;
    %% Definiamo i nodi: due topic e un microservizio
    topic_in("book-queue");
    microservice["prompt-enricher"];
    topic_out("enriched-prompts");
    
    %% Definiamo il flusso
    topic_in --> microservice;
    microservice --> topic_out;

    style microservice fill:#cce5ff,stroke:#3366cc,stroke-width:2px,color:#000;
    style topic_in fill:#ffcccc,stroke:#cc3333,stroke-width:2px,color:#000;
    style topic_out fill:#ffcccc,stroke:#cc3333,stroke-width:2px,color:#000;

```

Da Kafka riceviamo

```json
{
    "job_id": "String",
    "prompt": "String",
    "timestamp": "String"
}
```
Per poi ottenere dopo un'elaborazione un dato che inseriremo nel topic di output di Kafka.

```json
{
    "job_id": "String",
    "enriched_prompt": "String",
    "duration_ms": "Integer",
    "metrics": {
        "original_prompt_length": "Integer",
        "enriched_prompt_length": "Integer",
        "links_processed": "Integer",
        "links_failed": "Integer"
    },
    "error": "String"
}
```

Il topic `enriched-prompts` conterrà quindi tutti i dati elaborati dal microservizio.
