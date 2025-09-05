import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, from_json, to_json, struct, explode
from pyspark.sql.types import StringType, StructType, StructField, ArrayType
import dotenv

import designer
import book_filter
import schemas

dotenv.load_dotenv()

# --- CONFIGURAZIONE ROBUSTA ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
if not KAFKA_BOOTSTRAP_SERVERS:
    raise ValueError("La variabile d'ambiente KAFKA_BOOTSTRAP_SERVERS non è impostata.")

INPUT_TOPIC = "enriched-prompts"
OUTPUT_TOPIC_STRUCTURE = "book-structures"
OUTPUT_TOPIC_PARAGRAPHS = "paragraphs"

dirpath = os.path.dirname(__file__)

# --- INIZIALIZZAZIONE SPARK ---
spark = SparkSession.builder.appName("InstructionalDesignerDriver").getOrCreate()
spark.sparkContext.setLogLevel("WARN")
spark.sparkContext.addPyFile(os.path.join(dirpath, "designer.py"))
spark.sparkContext.addPyFile(os.path.join(dirpath, "book_filter.py"))

# --- LETTURA DA KAFKA (SOURCE) ---
# Questa sorgente è "replayable", il che è fondamentale per le garanzie.
streaming_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", INPUT_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

gen_book_structure_udf = udf(designer.enrich_prompt_and_collect_metrics, StringType())
filter_structure_udf = udf(book_filter.filter_book_structure, schemas.filtered_book_schema)

# --- ELABORAZIONE DATI ---
json_df = streaming_df.select(
    col("value").cast("string").alias("json_string")
).withColumn(
    "data", 
    from_json(col("json_string"), schemas.input_schema)
).select("data.*")

generated_book_structure_df = json_df.withColumn(
    "generated_book_structures",
    gen_book_structure_udf(col("enriched_prompt"), col("job_id"))
)

filtered_df = generated_book_structure_df.withColumn(
    "filtered_data",
    filter_structure_udf(col("generated_book_structures"))
)

def process_and_write_batch(batch_df, epoch_id):
    # batch_df è un DataFrame normale (non streaming!) che contiene i dati del micro-batch.
    # epoch_id è l'ID del micro-batch, utile per il logging.
    
    print(f"--- Processing Epoch/Batch ID: {epoch_id} ---")

    # Ora che siamo in un contesto batch, POSSIAMO e DOBBIAMO usare persist()
    # per evitare di ricalcolare batch_df per i due sink.
    batch_df.persist()

    try:
        # SINK 1: Logica per la struttura "scheletro"
        book_structure_to_write = batch_df.select(
            col("job_id").alias("key"),
            col("filtered_data.book_structure").alias("value")
        )
        
        print(f"Batch {epoch_id}: Writing {book_structure_to_write.count()} skeletons to Kafka...")
        
        book_structure_to_write.write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
            .option("topic", OUTPUT_TOPIC_STRUCTURE) \
            .save() # Nota: .save() non .start() perché siamo in un contesto batch

        # SINK 2: Logica per i paragrafi
        paragraphs_to_write = batch_df.select(
            col("job_id"),
            from_json(col("filtered_data.paragraphs"), ArrayType(schemas.paragraph_schema)).alias("paragraphs_array")
        ).select(
            col("job_id"),
            explode(col("paragraphs_array")).alias("paragraph_struct")
        ).select(
            col("paragraph_struct.paragraph_id").alias("key"),
            to_json(col("paragraph_struct")).alias("value")
        )

        print(f"Batch {epoch_id}: Writing {paragraphs_to_write.count()} paragraphs to Kafka...")

        paragraphs_to_write.write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
            .option("topic", OUTPUT_TOPIC_PARAGRAPHS) \
            .save() # Nota: .save()

    finally:
        # È buona norma rilasciare la cache alla fine di ogni batch
        batch_df.unpersist()


# 2. Usa foreachBatch nella tua query di streaming
#    Nota che ora hai UN SOLO writer stream e UN SOLO checkpoint principale.
query = filtered_df.writeStream \
    .foreachBatch(process_and_write_batch) \
    .outputMode("update") \
    .option("checkpointLocation", "/opt/spark/checkpoints/instructional-designer/main_pipeline") \
    .start()


# 3. Attendi la terminazione
query.awaitTermination()