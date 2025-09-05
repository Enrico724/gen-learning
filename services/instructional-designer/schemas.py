from pyspark.sql.types import StringType, StructType, StructField, ArrayType

input_schema = StructType([
    StructField("job_id", StringType(), True),
    StructField("enriched_prompt", StringType(), True),
])


filtered_book_schema = StructType([
    StructField("book_structure", StringType(), True),
    StructField("paragraphs", StringType(), True)
])

paragraph_schema = StructType([
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