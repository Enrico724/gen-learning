import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, from_json, to_json, struct
from pyspark.sql.types import StringType, StructType, StructField
import dotenv

import enricher
from pyspark.sql.types import ArrayType

dotenv.load_dotenv()

# --- CONFIGURAZIONE ROBUSTA ---

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
if not KAFKA_BOOTSTRAP_SERVERS:
    raise ValueError("La variabile d'ambiente KAFKA_BOOTSTRAP_SERVERS non è impostata.")

INPUT_TOPIC = "paragraphs"
OUTPUT_TOPIC = "enriched-paragraphs"
# In produzione, questo percorso DEVE essere su un file system fault-tolerant (HDFS, S3, etc.)
CHECKPOINT_LOCATION = "/opt/spark/checkpoints/paragraph-enricher"

dirpath = os.path.dirname(__file__)

# --- INIZIALIZZAZIONE SPARK ---
spark = SparkSession.builder.appName("ParagraphEnricherDriver").getOrCreate()
spark.sparkContext.setLogLevel("WARN")
spark.sparkContext.addPyFile(os.path.join(dirpath, "enricher.py"))

# --- LETTURA DA KAFKA (SOURCE) ---
# Questa sorgente è "replayable", il che è fondamentale per le garanzie.
streaming_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", INPUT_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# --- DEFINIZIONE DEGLI SCHEMI JSON ---
input_schema = StructType([
    StructField("paragraph_id", StringType(), True),
    StructField("titolo_paragrafo", StringType(), True),
    StructField("testo_segnaposto", StringType(), True),
    StructField("enrichment_info", StructType([
        StructField("focus", StringType(), True),
        StructField("tipo_arricchimento", ArrayType(StringType()), True),
        StructField("parole_chiave", ArrayType(StringType()), True),
        StructField("domande_guida", ArrayType(StringType()), True),
        StructField("livello_dettaglio", StringType(), True)
    ]), True)
])

enrich_paragraph_udf = udf(enricher.enrich_prompt_and_collect_metrics, StringType())

# --- ELABORAZIONE DATI ---
json_df = streaming_df.select(
    col("key").cast("string").alias("paragraph_id"),
    col("value").cast("string").alias("data")
)

enriched_df = json_df.withColumn(
    "processed_data",
    enrich_paragraph_udf(col("data"), col("paragraph_id"))
)

output_df = enriched_df.select(
    col("paragraph_id").alias("key"),
    col("processed_data").alias("value")
)

# output_df.writeStream.format("console").option("truncate", "false").start()

kafka_writer = output_df \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("topic", OUTPUT_TOPIC) \
    .option("checkpointLocation", CHECKPOINT_LOCATION) \
    .start()

# Attende la terminazione degli stream
spark.streams.awaitAnyTermination()
