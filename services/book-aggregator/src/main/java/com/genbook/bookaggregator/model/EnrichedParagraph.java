package com.genbook.bookaggregator.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class EnrichedParagraph {
    @JsonProperty("paragraph_id")
    private String paragraphId;
    @JsonProperty("enriched_paragraph")
    private String enrichedParagraph;

    // Getters and Setters
    public String getParagraphId() {
        return paragraphId;
    }

    public void setParagraphId(String paragraphId) {
        this.paragraphId = paragraphId;
    }

    public String getEnrichedParagraph() {
        return enrichedParagraph;
    }

    public void setEnrichedParagraph(String enrichedParagraph) {
        this.enrichedParagraph = enrichedParagraph;
    }
}
