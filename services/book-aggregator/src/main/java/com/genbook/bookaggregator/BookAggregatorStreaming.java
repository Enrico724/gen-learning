package com.genbook.bookaggregator;

import com.genbook.bookaggregator.model.BookStructure;
import com.genbook.bookaggregator.model.Chapter;
import com.genbook.bookaggregator.model.EnrichedParagraph;
import com.genbook.bookaggregator.model.SubChapter;
import com.genbook.bookaggregator.serdes.JsonSerde;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.processor.ProcessorContext;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.apache.kafka.streams.state.ValueAndTimestamp; // <-- Import necessario

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.stream.Collectors;

public class BookAggregatorStreaming {

    public static final String PARAGRAPHS_STORE_NAME = "paragraphs-store";

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "book-aggregator-app");
        String bootstrapServers = System.getenv("KAFKA_BOOTSTRAP_SERVERS");
        if (bootstrapServers == null || bootstrapServers.isEmpty()) {
            throw new IllegalStateException("Environment variable KAFKA_BOOTSTRAP_SERVERS is not set.");
        }
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(StreamsConfig.STATE_DIR_CONFIG, "/tmp/book-aggregator/state");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();

        final Serde<EnrichedParagraph> paragraphSerde = new JsonSerde<>(EnrichedParagraph.class);
        final Serde<BookStructure> bookStructureSerde = new JsonSerde<>(BookStructure.class);

        builder.globalTable(
                "enriched-paragraphs",
                Materialized.<String, EnrichedParagraph, KeyValueStore<Bytes, byte[]>>as(PARAGRAPHS_STORE_NAME)
                        .withKeySerde(Serdes.String())
                        .withValueSerde(paragraphSerde)
        );

        KStream<String, BookStructure> bookStructures = builder.stream(
                "book-structures",
                Consumed.with(Serdes.String(), bookStructureSerde)
        );

        KStream<String, BookStructure> generatedBooks = bookStructures.transformValues(
            new ValueTransformerWithKeySupplier<String, BookStructure, BookStructure>() {
                @Override
                public ValueTransformerWithKey<String, BookStructure, BookStructure> get() {
                    return new ValueTransformerWithKey<String, BookStructure, BookStructure>() {
                        // <-- MODIFICA 1: Specifichiamo che lo store contiene ValueAndTimestamp
                        private ReadOnlyKeyValueStore<String, ValueAndTimestamp<EnrichedParagraph>> paragraphStore;

                        @Override
                        public void init(ProcessorContext context) {
                            this.paragraphStore = context.getStateStore(PARAGRAPHS_STORE_NAME);
                        }

                        @Override
                        public BookStructure transform(String readOnlyKey, BookStructure inputBook) {
                            if (inputBook == null) {
                                return null;
                            }

                            for (Chapter chapter : inputBook.getCapitoli()) {
                                for (SubChapter subChapter : chapter.getSottocapitoli()) {
                                    for (String paragraphId : subChapter.getParagrafi()) {
                                        // <-- MODIFICA 2: Estraiamo prima ValueAndTimestamp, poi il valore effettivo
                                        ValueAndTimestamp<EnrichedParagraph> paragraphWithTs = paragraphStore.get(paragraphId);
                                        EnrichedParagraph paragraph = (paragraphWithTs != null) ? paragraphWithTs.value() : null;

                                        if (paragraph == null || paragraph.getEnrichedParagraph() == null || paragraph.getEnrichedParagraph().isEmpty()) {
                                            System.out.println("Paragrafo " + paragraphId + " non trovato per il libro " + inputBook.getTitoloLibro() + ". Aggregazione annullata.");
                                            return null;
                                        }
                                    }
                                }
                            }
                            
                            System.out.println("Tutti i paragrafi trovati per il libro " + inputBook.getTitoloLibro() + ". Procedo con l'aggregazione.");
                            BookStructure outputBook = new BookStructure();
                            outputBook.setTitoloLibro(inputBook.getTitoloLibro());
                            
                            List<Chapter> newChapters = new ArrayList<>();
                            for (Chapter inputChapter : inputBook.getCapitoli()) {
                                Chapter newChapter = new Chapter();
                                newChapter.setTitoloCapitolo(inputChapter.getTitoloCapitolo());

                                List<SubChapter> newSubChapters = new ArrayList<>();
                                for (SubChapter inputSubChapter : inputChapter.getSottocapitoli()) {
                                    SubChapter newSubChapter = new SubChapter();
                                    newSubChapter.setTitoloSottocapitolo(inputSubChapter.getTitoloSottocapitolo());

                                    List<String> paragraphTexts = inputSubChapter.getParagrafi().stream()
                                        // Estraiamo il valore anche qui
                                        .map(paragraphId -> paragraphStore.get(paragraphId).value().getEnrichedParagraph())
                                        .collect(Collectors.toList());

                                    newSubChapter.setParagrafi(paragraphTexts);
                                    newSubChapters.add(newSubChapter);
                                }
                                newChapter.setSottocapitoli(newSubChapters);
                                newChapters.add(newChapter);
                            }
                            outputBook.setCapitoli(newChapters);
                            return outputBook;
                        }

                        @Override
                        public void close() {}
                    };
                }
            }
        );

        generatedBooks.to("generated-books", Produced.with(Serdes.String(), bookStructureSerde));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        
        streams.setUncaughtExceptionHandler((thread, e) -> {
            System.err.println("FATAL ERROR in streams thread " + thread.getName() + ": " + e);
        });

        System.out.println("Avvio dell'applicazione Kafka Streams...");
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Chiusura dell'applicazione Kafka Streams...");
            streams.close();
        }));
    }
}