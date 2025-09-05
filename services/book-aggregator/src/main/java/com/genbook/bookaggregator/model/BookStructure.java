package com.genbook.bookaggregator.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class BookStructure {
    @JsonProperty("titolo_libro")
    private String titoloLibro;
    @JsonProperty("capitoli")
    private List<Chapter> capitoli;

    // Getters and Setters
    public String getTitoloLibro() {
        return titoloLibro;
    }

    public void setTitoloLibro(String titoloLibro) {
        this.titoloLibro = titoloLibro;
    }

    public List<Chapter> getCapitoli() {
        return capitoli;
    }

    public void setCapitoli(List<Chapter> capitoli) {
        this.capitoli = capitoli;
    }
}
