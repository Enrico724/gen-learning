import uuid
import time
import logging
import json
import requests

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.INFO
)

def send_message(prompt_text: str):
    """
    Crea un messaggio e lo invia a un server HTTP tramite una richiesta POST.
    """
    job_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))

    message = {
        "job_id": job_id,
        "prompt": prompt_text,
        "timestamp": timestamp,
        "links": []
    }
    logging.info(f"Messaggio creato (job_id: {job_id})")

    try:
        logging.info("Invio messaggio al server HTTP...")

        url = "http://localhost:3000/request-gen-book"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=message)

        logging.info(f"Risposta ricevuta: {response.text}")
    except Exception as e:
        logging.error(f"Impossibile inviare il messaggio: {e}")
        raise

if __name__ == "__main__":
    logging.info("Avvio del client HTTP.")

    try:
        prompt_da_inviare = input("Inserisci il prompt da inviare: ")
        send_message(prompt_da_inviare)
    except Exception as e:
        logging.critical(f"Si è verificato un errore fatale: {e}")
    
    logging.info("Il client HTTP ha terminato l'esecuzione.")
