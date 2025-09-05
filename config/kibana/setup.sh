#!/bin/sh

# Esci immediatamente se un comando fallisce
set -e

# --- Attendi che Kibana sia pronto ---
echo "Waiting for Kibana to be ready..."
until curl -s -f -u elastic:changeme http://kibana:5601/api/status -o /dev/null; do
  echo "Kibana is not ready yet (or credentials failed). Retrying in 5 seconds..."
  sleep 5
done

echo "Kibana is ready. Proceeding with dashboard import."

# --- Carica la Dashboard ---
# Nota che il percorso del file è quello *dentro* il container
curl -X POST "http://kibana:5601/api/saved_objects/_import?overwrite=true" \
     -H "kbn-xsrf: true" \
     -u elastic:changeme \
     --form "file=@/usr/share/kibana_assets/analisi-contenuto-libri.ndjson"

echo "Dashboard and related objects imported successfully!"