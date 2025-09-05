package com.genbook.bookaggregator.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class SubChapter {
    @JsonProperty("titolo_sottocapitolo")
    private String titoloSottocapitolo;
    @JsonProperty("paragrafi")
    private List<String> paragrafi;

    // Getters and Setters
    public String getTitoloSottocapitolo() {
        return titoloSottocapitolo;
    }

    public void setTitoloSottocapitolo(String titoloSottocapitolo) {
        this.titoloSottocapitolo = titoloSottocapitolo;
    }

    public List<String> getParagrafi() {
        return paragrafi;
    }

    public void setParagrafi(List<String> paragrafi) {
        this.paragrafi = paragrafi;
    }
}
