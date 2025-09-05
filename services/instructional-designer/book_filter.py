import logging
import uuid
import copy
import json

logger = logging.getLogger(__name__)
logging.getLogger("py4j").setLevel(logging.WARN)
logging.getLogger("pyspark").setLevel(logging.WARN)

def filter_book_structure(book_data_json: str) -> object:
    """
    Separa la struttura del libro in uno "scheletro" con riferimenti
    e una lista piatta di paragrafi.

    Args:
        book_data: Il dizionario contenente la struttura completa del libro.

    Returns:
        Una tupla contenente:
        - Il dizionario della struttura del libro modificata (scheletro).
        - Una lista di tutti gli oggetti paragrafo estratti.
    """

    json_data = json.loads(book_data_json)
    modified_book_structure = copy.deepcopy(json_data)

    extracted_paragraphs = []

    # Iteriamo attraverso la struttura per trovare i paragrafi
    if 'capitoli' in modified_book_structure:
        logger.debug("Found 'capitoli' in book structure")
        for chapter_idx, chapter in enumerate(modified_book_structure['capitoli']):
            logger.debug(f"Processing chapter {chapter_idx}")
            if 'sottocapitoli' in chapter:
                for subchapter_idx, subchapter in enumerate(chapter['sottocapitoli']):
                    logger.debug(f"Processing subchapter {subchapter_idx} in chapter {chapter_idx}")
                    if 'paragrafi' in subchapter and subchapter['paragrafi']:
                        logger.debug(f"Found {len(subchapter['paragrafi'])} paragraphs in subchapter {subchapter_idx}")
                        paragraph_references = []
                        # Estraiamo i paragrafi e li sostituiamo con i loro ID
                        for paragraph_idx, paragraph in enumerate(subchapter['paragrafi']):
                            paragraph_id = str(uuid.uuid4())
                            paragraph['paragraph_id'] = paragraph_id
                            extracted_paragraphs.append(paragraph)
                            paragraph_references.append(paragraph_id)
                            logger.debug(f"Extracted paragraph {paragraph_idx} with ID {paragraph_id}")
                        subchapter['paragrafi'] = paragraph_references
                        logger.debug(f"Replaced paragraphs with references in subchapter {subchapter_idx}")

    logger.info(f"Extraction complete: {len(extracted_paragraphs)} paragraphs extracted")
    logger.info(f"Extracted paragraphs: {json.dumps(extracted_paragraphs)}")
    return {
        "book_structure": json.dumps(modified_book_structure),
        "paragraphs": json.dumps(extracted_paragraphs)
    }
