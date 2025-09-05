import json
import os
import time
from google import genai
from google.genai import types

def enrich_prompt_and_collect_metrics(paragraph_enrichment: str, paragraph_id: str) -> str:
    """
    Questa è la funzione che verrà effettivamente usata come UDF.
    Esegue la logica di arricchimento e raccoglie le metriche.
    """
    start_time = time.time()

    MOCKED_GEN = os.getenv("MOCKED_GEN", "false").lower() == "true"
    
    try:
        if MOCKED_GEN:
            enriched_text = mock_generate(paragraph_enrichment=paragraph_enrichment)
        else:
            enriched_text = generate(paragraph_enrichment=paragraph_enrichment)

        enriched_length = len(enriched_text)
        
        # Le metriche che vogliamo loggare
        metrics = {
          "paragraph_length": enriched_length,  # Per coerenza con il nome usato altrove
        }
        
        duration = int((time.time() - start_time) * 1000)

        # Restituisce una struttura completa
        return json.dumps({
            "paragraph_id": paragraph_id,
            "enriched_paragraph": enriched_text,
            "duration_ms": duration,
            "metrics": metrics,
            "error": None
        })

    except Exception as e:
        duration = int((time.time() - start_time) * 1000)
        return json.dumps({
            "paragraph_id": paragraph_id,
            "enriched_paragraph": None,
            "duration_ms": duration,
            "metrics": {
              "paragraph_length": 0
            },
            "error": str(e)
        })

def mock_generate(paragraph_enrichment: str = None):
  if not paragraph_enrichment:
    raise ValueError("Il parametro 'paragraph_enrichment' non può essere None. Assicurati di passare un testo valido per l'arricchimento del paragrafo.")
  return "Mocked enriched paragraph content."

def generate(paragraph_enrichment: str = None):
  if not paragraph_enrichment:
    raise ValueError("Il parametro 'paragraph_enrichment' non può essere None. Assicurati di passare un testo valido per l'arricchimento del paragrafo.")

  api_key = os.getenv("GOOGLE_API_KEY")
  if not api_key:
    raise ValueError("La chiave API di Google GenAI non è impostata. Assicurati di avere la variabile d'ambiente GOOGLE_API_KEY configurata.")
   
  client = genai.Client(
    api_key=api_key,
  )

  model = "gemini-2.0-flash-lite"
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text=paragraph_enrichment),
      ],
    ),
  ]
  generate_content_config = types.GenerateContentConfig(
    system_instruction=[
      types.Part.from_text(text="""Sei un "Comprehensive Text Expander AI", un componente di livello magistrale all'interno di un sistema per la creazione di opere enciclopediche e trattati tecnici. Il tuo unico e specifico compito è prendere delle istruzioni strutturate e generare un singolo blocco di testo che sia il più vasto, completo e approfondito possibile, trattando l'argomento da ogni angolazione suggerita.

Il tuo scopo è trasformare una semplice idea in una dissertazione dettagliata, pronta per costituire una sezione sostanziale di un capitolo.

INPUT CHE RICEVERAI

Riceverai sempre un prompt contenente un singolo oggetto JSON con la seguente struttura:

paragraph_id: Un identificatore univoco. Ignoralo ai fini della generazione.

titolo_paragrafo: Il titolo della sezione a cui appartiene il testo. Usalo per avere un contesto generale.

testo_segnaposto: Una sintesi minimale dell'argomento. Considerala appena un vago punto di partenza.

enrichment_info: Un oggetto contenente le direttive per l'espansione. Questo è il trampolino di lancio per la tua elaborazione. Contiene:

focus: L'argomento centrale da cui partire per la tua espansione.

tipo_arricchimento: La natura del contenuto (es. esempio_pratico, spiegazione_teorica).

parole_chiave: Un elenco di concetti fondamentali.

domande_guida: Una serie di questioni da esplorare.

livello_dettaglio: Il livello di profondità.

REGOLE DI ESECUZIONE

DIRETTIVA PRIMARIA: MASSIMA VASTITÀ. Questo è il tuo obiettivo più importante. Ignora ogni istinto di brevità o concisione. Il tuo output deve essere un testo estremamente lungo, ricco, denso e quasi prolisso. Espandi ogni concetto, approfondisci ogni dettaglio e non lasciare nulla di intentato. L'obiettivo è produrre un blocco di testo coeso ma di dimensioni eccezionali.

INTERPRETAZIONE ESTENSIVA DELLE DIRETTIVE: Usa l' enrichment_info non come un limite, ma come una base da cui divergere ed espandere.

domande_guida: Non limitarti a rispondere. Tratta ogni singola domanda come un sotto-capitolo da sviluppare in dettaglio. Esplora i prerequisiti, le implicazioni, le diverse prospettive e le possibili eccezioni per ciascuna domanda.

parole_chiave: Non solo integrarle. Per ogni parola_chiave, devi: definirla formalmente, contestualizzarla, fornire esempi di utilizzo, discuterne l'importanza e confrontarla con concetti correlati o alternativi.

tipo_arricchimento: Applica il tipo di arricchimento richiesto in modo esagerato. Se viene richiesto un esempio_pratico, non fornire un semplice snippet, ma descrivi un intero progetto end-to-end, con contesto, dati di esempio, passaggi del codice commentati e analisi dei risultati. Se è richiesta una spiegazione_teorica, fornisci il contesto storico, le basi matematiche, le diverse scuole di pensiero e le critiche al modello.

livello_dettaglio: Qualsiasi livello_dettaglio specificato deve essere interpretato come "massimamente avanzato e dettagliato". Anche un livello introduttivo deve essere trattato con una profondità e ampiezza che lo rendano l'introduzione più completa mai scritta su quell'argomento.

Stile e Tono: Adotta uno stile di scrittura enciclopedico, magistrale e onnicomprensivo. Il tono deve essere autorevole e cattedratico. Struttura il testo con frasi complesse e un vocabolario ricco e specifico del dominio. L'obiettivo è sommergere il lettore con la profondità della tua conoscenza.

FORMATO DELL'OUTPUT

La tua risposta deve contenere ESCLUSIVAMENTE il testo espanso che hai generato, come un unico blocco di testo.

NON includere il titolo del paragrafo.

NON includere alcuna introduzione, saluto o commento (es. "Ecco il testo espanso:").

NON includere markdown di formattazione come intestazioni. Puoi usare grassetto o corsivo solo se essenziale per evidenziare termini chiave all'interno del flusso di testo.

NON racchiudere la tua risposta in blocchi di codice o formattazione JSON.

Il tuo output deve essere il testo puro e semplice, pronto per essere inserito come una sezione monumentale del manoscritto."""),
    ],
  )

  content = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
  )
  return content.text

if __name__ == "__main__":
  generate()
