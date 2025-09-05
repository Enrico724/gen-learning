import json
import os
import time
from google import genai
from google.genai import types

def enrich_prompt_and_collect_metrics(enriched_prompt: str, job_id: str) -> str:
    """
    Questa è la funzione che verrà effettivamente usata come UDF.
    Esegue la logica di arricchimento e raccoglie le metriche.
    """
    start_time = time.time()

    MOCKED_GEN = os.getenv("MOCKED_GEN", "false").lower() == "true"
    
    try:
        # Usa la funzione che preferisci (mock o reale)
        if MOCKED_GEN:
            book_structure = mock_gen_book_structure(enriched_prompt=enriched_prompt)
        else:
            book_structure = gen_book_structure(enriched_prompt=enriched_prompt)

        # Le metriche che vogliamo loggare
        book_structure_data = json.loads(book_structure)
        chapter_qty = len(book_structure_data.get("capitoli", []))
        subchapter_qty = sum(len(chapter.get("sottocapitoli", [])) for chapter in book_structure_data.get("capitoli", []))
        paragraphs = sum(
            len(subchapter.get("paragrafi", []))
            for chapter in book_structure_data.get("capitoli", [])
            for subchapter in chapter.get("sottocapitoli", [])
        )
        
        metrics = {
            "chapter_qty": chapter_qty,
            "subchapter_qty": subchapter_qty,
            "paragraphs": paragraphs
        }
        
        duration = int((time.time() - start_time) * 1000)

        # Restituisce una struttura completa
        return json.dumps({
            "job_id": job_id,
            "titolo_libro": book_structure_data.get("titolo_libro"),
            "capitoli": book_structure_data.get("capitoli"),
            "duration_ms": duration,
            "metrics": metrics,
            "error": None
        })

    except Exception as e:
        duration = int((time.time() - start_time) * 1000)
        return json.dumps({
            "job_id": job_id,
            "titolo_libro": None,
            "capitoli": [],
            "duration_ms": duration,
            "metrics": {
                "chapter_qty": 0,
                "subchapter_qty": 0,
                "paragraphs": 0
            },
            "error": str(e)
        })


def mock_gen_book_structure(enriched_prompt: str = None) -> str:
    """
    Mock function to simulate the generation of book structure.
    This is a placeholder for the actual implementation that would
    interact with the Google Gemini API.
    
    Args:
        enriched_prompt (str): The enriched prompt for book structure generation.
    
    Returns:
        str: A JSON string representing the book structure.
    """
    if enriched_prompt is None:
        raise ValueError("enriched_prompt must be provided")
    
    # Simulated response
    return json.dumps({
        "titolo_libro": "Esempio di Libro",
        "capitoli": [
            {
                "titolo_capitolo": "Capitolo 1",
                "sottocapitoli": [
                    {
                        "titolo_sottocapitolo": "Sottocapitolo 1.1",
                        "paragrafi": [
                            {
                                "titolo_paragrafo": "Paragrafo 1.1.1",
                                "testo_segnaposto": "Testo del paragrafo 1.1.1",
                                "enrichment_info": {
                                    "focus": "Focus del paragrafo",
                                    "tipo_arricchimento": ["definizione_tecnica"],
                                    "parole_chiave": ["parola1", "parola2"],
                                    "domande_guida": ["Domanda 1", "Domanda 2"],
                                    "livello_dettaglio": "introduttivo"
                                }
                            },
                            {
                                "titolo_paragrafo": "Paragrafo 1.1.2",
                                "testo_segnaposto": "Testo del paragrafo 1.1.2",
                                "enrichment_info": {
                                    "focus": "Focus del paragrafo",
                                    "tipo_arricchimento": ["esempio_pratico"],
                                    "parole_chiave": ["parola3", "parola4"],
                                    "domande_guida": ["Domanda 3", "Domanda 4"],
                                    "livello_dettaglio": "approfondito"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    })

def gen_book_structure(enriched_prompt: str = None) -> str:
  if enriched_prompt is None:
    raise ValueError("enriched_prompt must be provided")
  
  client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
  )

  model = "gemini-2.5-flash-lite"
  contents = [
      types.Content(
          role="user",
          parts=[
              types.Part.from_text(text=enriched_prompt),
          ],
      ),
  ]
  generate_content_config = types.GenerateContentConfig(
      thinking_config = types.ThinkingConfig(
          thinking_budget=0,
      ),
      response_mime_type="application/json",
      response_schema=genai.types.Schema(
          type = genai.types.Type.OBJECT,
          required = ["titolo_libro", "capitoli"],
          properties = {
              "titolo_libro": genai.types.Schema(
                  type = genai.types.Type.STRING,
                  description = "Il titolo principale del libro.",
              ),
              "capitoli": genai.types.Schema(
                  type = genai.types.Type.ARRAY,
                  description = "Una lista di tutti i capitoli che compongono il libro.",
                  items = genai.types.Schema(
                      type = genai.types.Type.OBJECT,
                      required = ["titolo_capitolo", "sottocapitoli"],
                      properties = {
                          "titolo_capitolo": genai.types.Schema(
                              type = genai.types.Type.STRING,
                              description = "Il titolo del capitolo.",
                          ),
                          "sottocapitoli": genai.types.Schema(
                              type = genai.types.Type.ARRAY,
                              description = "Una lista dei sottocapitoli appartenenti a questo capitolo.",
                              items = genai.types.Schema(
                                  type = genai.types.Type.OBJECT,
                                  required = ["titolo_sottocapitolo", "paragrafi"],
                                  properties = {
                                      "titolo_sottocapitolo": genai.types.Schema(
                                          type = genai.types.Type.STRING,
                                          description = "Il titolo del sottocapitolo.",
                                      ),
                                      "paragrafi": genai.types.Schema(
                                          type = genai.types.Type.ARRAY,
                                          description = "Una lista dei paragrafi che compongono il sottocapitolo.",
                                          items = genai.types.Schema(
                                              type = genai.types.Type.OBJECT,
                                              required = ["titolo_paragrafo", "testo_segnaposto", "enrichment_info"],
                                              properties = {
                                                  "titolo_paragrafo": genai.types.Schema(
                                                      type = genai.types.Type.STRING,
                                                      description = "Il titolo specifico del paragrafo.",
                                                  ),
                                                  "testo_segnaposto": genai.types.Schema(
                                                      type = genai.types.Type.STRING,
                                                      description = "Una breve descrizione del contenuto previsto per il paragrafo.",
                                                  ),
                                                  "enrichment_info": genai.types.Schema(
                                                      type = genai.types.Type.OBJECT,
                                                      description = "Metadati e istruzioni per l'arricchimento del contenuto del paragrafo.",
                                                      required = ["focus", "tipo_arricchimento", "parole_chiave", "domande_guida", "livello_dettaglio"],
                                                      properties = {
                                                          "focus": genai.types.Schema(
                                                              type = genai.types.Type.STRING,
                                                              description = "L'argomento o concetto principale su cui il paragrafo deve concentrarsi.",
                                                          ),
                                                          "tipo_arricchimento": genai.types.Schema(
                                                              type = genai.types.Type.ARRAY,
                                                              description = "Una lista di tipologie di contenuto da generare per arricchire il testo.",
                                                              items = genai.types.Schema(
                                                                  type = genai.types.Type.STRING,
                                                                  enum = ["definizione_tecnica", "esempio_pratico", "immagine_esplicativa", "case_study"],
                                                              ),
                                                          ),
                                                          "parole_chiave": genai.types.Schema(
                                                              type = genai.types.Type.ARRAY,
                                                              description = "Una lista di parole chiave pertinenti al contenuto del paragrafo.",
                                                              items = genai.types.Schema(
                                                                  type = genai.types.Type.STRING,
                                                              ),
                                                          ),
                                                          "domande_guida": genai.types.Schema(
                                                              type = genai.types.Type.ARRAY,
                                                              description = "Domande a cui il contenuto del paragrafo dovrebbe rispondere.",
                                                              items = genai.types.Schema(
                                                                  type = genai.types.Type.STRING,
                                                              ),
                                                          ),
                                                          "livello_dettaglio": genai.types.Schema(
                                                              type = genai.types.Type.STRING,
                                                              description = "Il livello di profondità richiesto per la trattazione dell'argomento.",
                                                              enum = ["introduttivo", "approfondito", "tecnico"],
                                                          ),
                                                      },
                                                  ),
                                              },
                                          ),
                                      ),
                                  },
                              ),
                          ),
                      },
                  ),
              ),
          },
      ),
      system_instruction=[
          types.Part.from_text(text="Ruolo: Sei un assistente AI esperto in architettura dell'informazione e pianificazione editoriale. Il tuo compito è tradurre una richiesta testuale in una struttura dati JSON ben definita. Obiettivo: Analizza il testo di input fornito dall'utente, che descrive l'indice o la struttura di un libro. Da questa analisi, devi generare un output esclusivamente in formato JSON che rappresenti la struttura gerarchica del libro in capitoli, sottocapitoli, paragrafi e, se necessario, sottoparagrafi.")
      ],
  )
  
  content = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
  )
  return json.dumps(content.parsed)
