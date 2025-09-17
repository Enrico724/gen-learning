+++
weight = 3
+++

# Flusso Dati

```mermaid
graph LR;
    topic_in(paragraphs);
    microservice[paragraph-enricher];
    topic_out(enriched-paragraphs);
    
    topic_in --> microservice;
    microservice --> topic_out;

    style microservice fill:#cce5ff,stroke:#3366cc,stroke-width:2px,color:#000;
    style topic_in fill:#ffcccc,stroke:#cc3333,stroke-width:2px,color:#000;
    style topic_out fill:#ffcccc,stroke:#cc3333,stroke-width:2px,color:#000;
```

Da Kafka riceviamo

```json
{
    "paragraph_id": "String",
    "titolo_paragrafo": "String",
    "testo_segnaposto": "String",
    "enrichment_info": {
        "focus": "String",
        "tipo_arricchimento": ["String"],
        "parole_chiave": ["String"],
        "domande_guida": ["String"],
        "livello_dettaglio": "String"
    }
}
```

Dopo l'elaborazione, otteniamo un dato che viene inserito direttamente nel topic di output di Kafka e che include anche le metriche relative al paragrafo generato.

```json
{
    "paragraph_id": "String",
    "enriched_paragraph": "String",
    "metrics": {
        "duration_ms": "Integer",
        "paragraph_length": "Integer"
    }
}
```
