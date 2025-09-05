import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, from_json, to_json, struct
from pyspark.sql.types import StringType, StructType, StructField, ArrayType
import dotenv

import enricher

dotenv.load_dotenv()

# --- CONFIGURAZIONE ROBUSTA ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
if not KAFKA_BOOTSTRAP_SERVERS:
    raise ValueError("La variabile d'ambiente KAFKA_BOOTSTRAP_SERVERS non è impostata.")

INPUT_TOPIC = "book-queue"
OUTPUT_TOPIC = "enriched-prompts"
# In produzione, questo percorso DEVE essere su un file system fault-tolerant (HDFS, S3, etc.)
CHECKPOINT_LOCATION = "/opt/spark/checkpoints/prompt-enricher"

dirpath = os.path.dirname(__file__)

# --- INIZIALIZZAZIONE SPARK ---
spark = SparkSession.builder.appName("PromptEnricherDriver").getOrCreate()
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
    StructField("job_id", StringType(), True),
    StructField("prompt", StringType(), True),
    StructField("links", ArrayType(StringType()), True),
    StructField("timestamp", StringType(), True)
])

processed_schema = StructType([
    StructField("job_id", StringType(), True),
    StructField("enriched_prompt", StringType(), True),
    StructField("duration_ms", StringType(), True),
    StructField("metrics", StructType([
        StructField("original_prompt_length", StringType(), True),
        StructField("enriched_prompt_length", StringType(), True),
        StructField("links_processed", StringType(), True),
        StructField("links_failed", StringType(), True)
    ]), True),
    StructField("error", StringType(), True)
])

enrich_prompt_udf = udf(enricher.enrich_prompt_and_collect_metrics, processed_schema)

# --- ELABORAZIONE DATI ---
json_df = streaming_df.select(col("value").cast("string").alias("json_string")) \
    .withColumn("data", from_json(col("json_string"), input_schema)) \
    .select("data.*")

enriched_df = json_df.withColumn(
    "processed_prompt",
    enrich_prompt_udf(col("prompt"), col("job_id"), col("links"))
)

output_df = enriched_df.select(
    col("job_id").alias("key"),
    to_json(
        struct(
            col("job_id"),
            col("processed_prompt.enriched_prompt").alias("enriched_prompt"),
            col("processed_prompt.duration_ms").alias("duration_ms"),
            col("processed_prompt.metrics").alias("metrics"),
            col("processed_prompt.error").alias("error")
        )
    ).alias("value")
)

# output_df.writeStream.format("console").option("truncate", "false").start()


# --- SCRITTURA SU KAFKA (SINK) ---
# Il sink Kafka di Spark è transazionale e garantisce la scrittura "exactly-once"
# grazie all'uso di un producer idempotente e alla gestione tramite checkpoint.
kafka_writer = output_df \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("topic", OUTPUT_TOPIC) \
    .option("checkpointLocation", CHECKPOINT_LOCATION) \
    .start()

# Attende la terminazione degli stream
spark.streams.awaitAnyTermination()
