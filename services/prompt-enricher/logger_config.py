import logging
import logstash
from pythonjsonlogger import jsonlogger
import os

# --- 1. CONFIGURAZIONE ---
# Carica le impostazioni dall'ambiente per maggiore flessibilità.
# Se le variabili d'ambiente non sono impostate, usa dei valori di default.
LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', 'localhost')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT', 5959))
SERVICE_NAME = os.getenv('SERVICE_NAME', 'prompt-enricher')

# --- 2. FILTRO PER ARRICCHIMENTO DEI LOG ---
# Un filtro permette di aggiungere informazioni contestuali a *tutti* i record di log
# generati da questo logger. È il modo migliore per aggiungere dati statici come il nome del servizio.
class ServiceNameFilter(logging.Filter):
    """Aggiunge il campo 'service_name' ad ogni record di log."""
    def filter(self, record):
        record.service_name = SERVICE_NAME
        return True

# --- 3. FORMATTATORE JSON ---
# Utilizziamo JsonFormatter per garantire che l'output sia in formato JSON,
# ideale per sistemi di aggregazione log come Logstash ed Elasticsearch.
# - rinominiamo 'asctime' in '@timestamp' e 'levelname' in 'log_level' per
#   compatibilità con gli standard di Logstash/Elastic.
formatter = jsonlogger.JsonFormatter(
    # Definiamo i campi base che vogliamo nel messaggio formattato
    '%(asctime)s %(levelname)s %(name)s %(message)s',
    rename_fields={'asctime': '@timestamp', 'levelname': 'log_level'}
)

# --- 4. HANDLERS (DESTINAZIONI DEI LOG) ---

# Handler per inviare i log a Logstash tramite TCP
# `version=1` indica che i messaggi saranno formattati secondo lo schema Logstash v1.
logstash_handler = logstash.TCPLogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, version=1)
logstash_handler.setFormatter(formatter)

# Handler per scrivere i log sulla console (utile per il debug in locale)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


# --- 5. CREAZIONE E CONFIGURAZIONE DEL LOGGER ---
# Otteniamo l'istanza del logger. Usare un nome specifico è una buona pratica.
logger = logging.getLogger('structured-logger')
logger.setLevel(logging.INFO) # Impostiamo il livello minimo di log da processare

# Aggiungiamo il filtro per arricchire i