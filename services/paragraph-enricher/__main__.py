import os
import dotenv

dotenv.load_dotenv()

KAFKA_VERSION = os.getenv("KAFKA_VERSION")

if __name__ == "__main__":
    if not KAFKA_VERSION:
        raise ValueError("La variabile d'ambiente KAFKA_VERSION non è impostata.")

    dirpath = os.path.dirname(__file__)
    os.system(f"spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:{KAFKA_VERSION} {dirpath}/driver.py")