# Esegui questi comandi uno per uno. Se uno dà errore perché il tipo non è 'kafkatopic', 
# dovrai trovare il tipo corretto con il comando del Passaggio 1.

kubectl patch kafkatopic book-queue -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'
kubectl patch kafkatopic book-structures -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'
kubectl patch kafkatopic enriched-paragraphs -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'
kubectl patch kafkatopic enriched-prompts -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'
kubectl patch kafkatopic generated-books -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'
kubectl patch kafkatopic paragraphs -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'

# Potrebbe esserci anche la risorsa 'Kafka' stessa o altre
# Se 'genbook' è una risorsa di tipo 'Kafka', il comando sarebbe:
# kubectl patch kafka genbook -n genbook -p '{"metadata":{"finalizers":[]}}' --type='merge'