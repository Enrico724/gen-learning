+++
weight = 5
title = "Book Producer"
description = "Descrizione del microservizio book-producer"
+++

## Flusso Dati

Il microservizio **book-producer** è responsabile della generazione di file PDF a partire dai dati ricevuti. Il flusso dei dati è rappresentato nel diagramma seguente:

```mermaid
graph LR;
    %% Definiamo i nodi
    %% La sintassi (testo) crea un nodo con angoli arrotondati (ovale)
    topic_in(generated-books);
    microservice[book-producer];
    s3["Bucket Storage"]
    
    %% Definiamo il flusso
    topic_in --> microservice;
    microservice --> s3

    style microservice fill:#cce5ff,stroke:#3366cc,stroke-width:2px,color:#000;
    style topic_in fill:#ffcccc,stroke:#cc3333,stroke-width:2px,color:#000;
    style s3 fill:#f2f2f2,stroke:#595959,stroke-width:2px,color:#000;
    
```

### Dettagli del Flusso

1. **Input**: Il microservizio riceve i dati dal topic `generated-books`.
2. **Elaborazione**: I dati vengono processati dal microservizio `book-producer`.
3. **Output**: Il risultato dell'elaborazione è un file PDF generato.

Questo microservizio è un componente chiave per la produzione di documenti PDF automatizzati.