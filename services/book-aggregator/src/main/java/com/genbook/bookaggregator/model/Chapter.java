package com.genbook.bookaggregator.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class Chapter {
    @JsonProperty("titolo_capitolo")
    private String titoloCapitolo;
    @JsonProperty("sottocapitoli")
    private List<SubChapter> sottocapitoli;

    // Getters and Setters
    public String getTitoloCapitolo() {
        return titoloCapitolo;
    }

    public void setTitoloCapitolo(String titoloCapitolo) {
        this.titoloCapitolo = titoloCapitolo;
    }

    public List<SubChapter> getSottocapitoli() {
        return sottocapitoli;
    }

    public void setSottocapitoli(List<SubChapter> sottocapitoli) {
        this.sottocapitoli = sottocapitoli;
    }
}
