## Topic di Kafka

```mermaid
graph LR;
    %% Riquadro per raggruppare i topic di Kafka
    subgraph KAFKA
        direction TB;

        %% Lista dei topic (ovals)
        t1(book-queue);
        t2(enriched-prompt);
        t3(book-structures);
        t4(paragraphs);
        t5(enriched-paragraphs);
        t6(generated-books);
    end

```

I topic di Kafka rappresentano i canali di comunicazione utilizzati per lo scambio di messaggi tra i vari microservizi. Ogni topic è identificato da un nome univoco e funge da buffer per i dati che vengono prodotti e consumati dai servizi. Nel diagramma sopra, i topic sono rappresentati come ovali e sono raggruppati all'interno del riquadro "KAFKA". 

Ecco una breve descrizione dei topic:
- **book-queue**: Contiene le richieste iniziali inviate dall'API Gateway.
- **enriched-prompt**: Memorizza i prompt arricchiti dal microservizio `prompt-enricher`.
- **book-structures**: Contiene le strutture dei libri generate dal microservizio `instructional-designer`.
- **paragraphs**: Raccoglie i paragrafi generati dal microservizio `instructional-designer`.
- **enriched-paragraphs**: Contiene i paragrafi arricchiti dal microservizio `paragraph-enricher`.
- **generated-books**: Memorizza i libri completi generati dal microservizio `book-aggregator`.

## Flusso lavorativo

```mermaid
graph LR;
    %% Start
    api_gateway[API Gateway];

    %% Topics (ovals)
    t1(book-queue);
    t2(enriched-prompt);
    t3(book-structures);
    t4(paragraphs);
    t5(enriched-paragraphs);
    t6(generated-books);

    %% Microservices (rectangles)
    ms1[prompt-enricher];
    ms2[instructional-designer];
    ms3[paragraph-enricher];
    ms4[book-aggregator];
    ms5[book-producer];

    %% Flow
    api_gateway --> t1;
    t1 --> ms1;
    ms1 --> t2;
    t2 --> ms2;
    ms2 --> t3;
    ms2 --> t4;
    t4 --> ms3;
    ms3 --> t5;
    t3 --> ms4;
    t5 --> ms4;
    ms4 --> t6;
    t6 --> ms5;
```

Il flusso lavorativo illustra come i dati si muovono attraverso i vari microservizi e i topic di Kafka. Ecco una descrizione passo-passo del processo:

1. **API Gateway**: Riceve le richieste iniziali e le invia al topic `book-queue`.
2. **Prompt Enricher**: Consuma i messaggi da `book-queue`, arricchisce i prompt e li pubblica su `enriched-prompt`.
3. **Instructional Designer**: Consuma i prompt arricchiti da `enriched-prompt` e genera sia le strutture dei libri (`book-structures`) che i paragrafi (`paragraphs`).
4. **Paragraph Enricher**: Consuma i paragrafi da `paragraphs`, li arricchisce e li pubblica su `enriched-paragraphs`.
5. **Book Aggregator**: Combina le strutture dei libri (`book-structures`) e i paragrafi arricchiti (`enriched-paragraphs`) per creare libri completi, che vengono pubblicati su `generated-books`.
6. **Book Producer**: Consuma i libri completi da `generated-books` e li rende disponibili per ulteriori utilizzi o distribuzione.

Questo flusso garantisce una pipeline modulare e scalabile per la generazione e l'arricchimento dei contenuti. Ogni microservizio è responsabile di un compito specifico, facilitando la manutenzione e l'estensibilità del sistema.